"""Toyota Connected Services Controller"""
import logging
from typing import Optional
from datetime import datetime
import httpx


from .const import (
    BASE_URL,
    BASE_URL_CARS,
    CUSTOMERPROFILE,
    ENDPOINT_AUTH,
    PASSWORD,
    TIMEOUT,
    TOKEN,
    USERNAME,
    UUID,
    HTTP_OK,
    HTTP_NO_CONTENT,
    HTTP_UNAUTHORIZED,
    TOKEN_DURATION,
    SUPPORTED_REGIONS,
)
from .exceptions import (
    ToyotaLoginError,
)
from .utils import is_valid_uuid, is_valid_token

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Controller:
    """Controller class."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        locale: str,
        region: str,
        username: str,
        password: str,
    ) -> None:
        """Toyota Controller"""

        self.token = None
        self.uuid = None
        self.token_date: Optional[datetime] = None

        self.locale: str = locale
        self.region: str = region

        self.username: str = username
        self.password: str = password

    @staticmethod
    def __token_has_expired(creation_dt, duration) -> bool:
        """Checks if token has expired."""
        if creation_dt is not None:
            return datetime.now().timestamp() - creation_dt.timestamp() > duration
        return True

    def invalidate_token(self):
        """Invalidates the current access token."""
        self.token = None
        self.token_date = None

    def get_base_url(self):
        """Returns base url"""
        return SUPPORTED_REGIONS[self.region][BASE_URL]

    def get_base_url_cars(self):
        """Returns base url for get_vehicles_endpoint"""
        return SUPPORTED_REGIONS[self.region][BASE_URL_CARS]

    def get_auth_endpoint(self):
        """Returns auth endpoint"""
        return SUPPORTED_REGIONS[self.region][ENDPOINT_AUTH]

    async def get_token(self) -> tuple:
        """Performs login to toyota servers and retrieves token and uuid for the account."""

        if self.token is None or self.__token_has_expired(
            self.token_date, TOKEN_DURATION
        ):
            headers = {
                "X-TME-BRAND": "TOYOTA",
                "X-TME-LC": self.locale,
                "Accept": "application/json, text/plain, */*",
                "Sec-Fetch-Dest": "empty",
                "Content-Type": "application/json;charset=UTF-8",
            }

            # Cannot authenticate with aiohttp (returns 415),
            # but it works with requests.
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.get_auth_endpoint(),
                    headers=headers,
                    json={USERNAME: self.username, PASSWORD: self.password},
                )
                if response.status_code == HTTP_OK:
                    result = response.json()

                    if TOKEN not in result or UUID not in result[CUSTOMERPROFILE]:
                        _LOGGER.error("[!] Could not get token or UUID.")

                    token = result.get(TOKEN)
                    uuid = result[CUSTOMERPROFILE][UUID]

                    if is_valid_token(token) and is_valid_uuid(uuid):
                        self.uuid = uuid
                        self.token = token
                        self.token_date = datetime.now()
                else:
                    raise ToyotaLoginError(
                        "Login failed, check your credentials! {}".format(response.text)
                    )

        return self.token

    async def get(self, endpoint: str, headers=None, params=None):
        """Make the request."""

        token = await self.get_token()

        if headers is None:
            headers = {}
        headers.update(
            {
                "Cookie": f"iPlanetDirectoryPro={token}",
                "uuid": self.uuid,
                "Accept": "application/json, text/plain, */*",
                "Sec-Fetch-Dest": "empty",
                "X-TME-BRAND": "TOYOTA",
                "X-TME-LC": self.locale,
                "X-TME-LOCALE": self.locale,
                "X-TME-TOKEN": token,
            }
        )
        async with httpx.AsyncClient() as client:
            resp = await client.get(endpoint, headers=headers, params=params, timeout=TIMEOUT)

            if resp.status_code == HTTP_OK:
                result = resp.json()
            elif resp.status_code == HTTP_NO_CONTENT:
                result = None  # This prevents raising or logging an error if the user has not setup Connected Services
            elif resp.status_code == HTTP_UNAUTHORIZED:
                self.invalidate_token()
                result = await self.get(endpoint, headers)
            else:
                _LOGGER.error("HTTP: %i - %s", resp.status_code, resp.text)
                result = None

            return result

    async def put(self, endpoint: str, body: dict, headers=None):
        """Make the request."""

        token = await self.get_token()

        if headers is None:
            headers = {}
        headers.update(
            {
                "Accept": "application/json, text/plain, */*",
                "Sec-Fetch-Dest": "empty",
                "X-TME-BRAND": "TOYOTA",
                "X-TME-LC": self.locale,
                "X-TME-TOKEN": token,
            }
        )

        async with httpx.AsyncClient() as client:
            resp = await client.put(
                endpoint, json=body, headers=headers, timeout=TIMEOUT
            )

            if resp.status_code == HTTP_OK:
                result = resp.json()
            elif resp.status_code == HTTP_NO_CONTENT:
                result = None # This prevents raising or logging an error if the user has not setup Connected Services
            elif resp.status_code == HTTP_UNAUTHORIZED:
                self.invalidate_token()
                result = await self.get(endpoint, headers)
            else:
                _LOGGER.error("HTTP: %i - %s", resp.status_code, resp.text)
                result = None

            return result

    async def set_vehicle_alias_endpoint(self, new_alias: str, vehicle_id: int) -> dict:
        """Set vehicle alias."""

        return await self.put(
            f"{self.get_base_url_cars()}/api/users/{self.uuid}/vehicles/{vehicle_id}",
            {"id": vehicle_id, "alias": new_alias},
        )

    async def get_vehicles_endpoint(self) -> list:
        """Retrieves list of cars you have registered with MyT"""

        arguments = "?services=uio&legacy=true"

        return await self.get(
            f"{self.get_base_url_cars()}/vehicle/user/{self.uuid}/vehicles{arguments}"
        )

    async def get_connected_services_endpoint(self, vin: str) -> dict:
        """Get information about connected services for the given car."""

        arguments = "?legacy=true&services=fud,connected"

        return await self.get(
            f"{self.get_base_url_cars()}/vehicle/user/{self.uuid}/vehicle/{vin}{arguments}"
        )

    async def get_odometer_endpoint(self, vin: str) -> list:
        """Get information from odometer."""

        return await self.get(f"{self.get_base_url()}/vehicle/{vin}/addtionalInfo")

    async def get_parking_endpoint(self, vin: str) -> dict:
        """Get where you have parked your car."""

        return await self.get(
            f"{self.get_base_url()}/users/{self.uuid}/vehicle/location", {"VIN": vin}
        )

    async def get_vehicle_status_endpoint(self, vin: str) -> dict:
        """Get information about the vehicle."""

        return await self.get(
            f"{self.get_base_url()}/vehicles/{vin}/remoteControl/status"
        )

    async def get_driving_statistics_endpoint(self, vin: str, from_date, interval="day") -> list:
        """Get driving statistic"""

        params = {'from': from_date, 'calendarInterval': interval}

        return await self.get(
            f"{self.get_base_url()}/v2/trips/summarize",
            {"vin": vin},
            params
        )
