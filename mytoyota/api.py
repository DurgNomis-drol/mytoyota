"""Toyota Connected Services Controller"""
import logging
from typing import Optional, Union
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
    SUPPORTED_REGIONS,
    TOKEN_VALID_URL,
    TOKEN_DURATION,
    HTTP_BAD_REQUEST,
    RETURNED_BAD_REQUEST,
)
from .exceptions import (
    ToyotaLoginError,
)
from .utils import is_valid_token

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Controller:
    """Controller class."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        locale: str,
        region: str,
        username: str,
        password: str,
        uuid: str,
    ) -> None:
        """Toyota Controller"""

        self.token = None
        self.token_expiration: Optional[datetime] = None
        self.uuid = None

        if uuid is not None:
            self.uuid = uuid

        self.locale: str = locale
        self.region: str = region

        self.username: str = username
        self.password: str = password

    def get_base_url(self) -> str:
        """Returns base url"""
        return SUPPORTED_REGIONS[self.region][BASE_URL]

    def get_base_url_cars(self) -> str:
        """Returns base url for get_vehicles_endpoint"""
        return SUPPORTED_REGIONS[self.region][BASE_URL_CARS]

    def get_auth_endpoint(self) -> str:
        """Returns auth endpoint"""
        return SUPPORTED_REGIONS[self.region][ENDPOINT_AUTH]

    def get_auth_valid_endpoint(self) -> str:
        """Returns token is valid endpoint"""
        return SUPPORTED_REGIONS[self.region][TOKEN_VALID_URL]

    async def get_uuid(self) -> str:
        """Returns uuid"""
        return self.uuid

    @staticmethod
    def _has_expired(creation_dt, duration) -> bool:
        """Checks if an specified token/object has expired"""
        return datetime.now().timestamp() - creation_dt.timestamp() > duration

    async def is_token_valid(self) -> bool:
        """Checks if token is valid"""

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.get_auth_valid_endpoint(),
                json={TOKEN: self.token},
            )
            if response.status_code == HTTP_OK:
                result = response.json()

                if result["valid"]:
                    self.token_expiration = datetime.now()
                    return True
                return False

            raise ToyotaLoginError(
                "Error when trying to check token: {}".format(response.text)
            )

    async def get_new_token(self) -> str:
        """Performs login to toyota servers and retrieves token and uuid for the account."""

        headers = {
            "X-TME-BRAND": "TOYOTA",
            "X-TME-LC": self.locale,
            "Accept": "application/json, text/plain, */*",
            "Sec-Fetch-Dest": "empty",
            "Content-Type": "application/json;charset=UTF-8",
        }

        # Cannot authenticate with aiohttp (returns 415),
        # but it works with httpx.
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

                if is_valid_token(token):
                    self.uuid = uuid
                    self.token = token
                    self.token_expiration = datetime.now()
            else:
                raise ToyotaLoginError(
                    "Login failed, check your credentials! {}".format(response.text)
                )

        return self.token

    async def get(
        self, endpoint: str, headers=None, params=None
    ) -> Union[dict, list, None]:
        """Make the request."""

        if self.token is None or self._has_expired(
            self.token_expiration, TOKEN_DURATION
        ):
            if await self.is_token_valid() is False:
                await self.get_new_token()

        if headers is None:
            headers = {}
        headers.update(
            {
                "Cookie": f"iPlanetDirectoryPro={self.token}",
                "uuid": self.uuid,
                "Accept": "application/json, text/plain, */*",
                "Sec-Fetch-Dest": "empty",
                "X-TME-BRAND": "TOYOTA",
                "X-TME-LC": self.locale,
                "X-TME-LOCALE": self.locale,
                "X-TME-TOKEN": self.token,
            }
        )
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                endpoint, headers=headers, params=params, timeout=TIMEOUT
            )

            if resp.status_code == HTTP_OK:
                result = resp.json()
            elif resp.status_code == HTTP_BAD_REQUEST:
                # Reason for getting HTTP: 400
                # - Invalid interval
                # - If from_date is the same as to_date.
                # - Probably something else.
                # We also log the error if the error is something else.
                result = RETURNED_BAD_REQUEST
                _LOGGER.error(resp.text)
            elif resp.status_code == HTTP_NO_CONTENT:
                # This prevents raising or logging an error
                # if the user has not setup Connected Services
                result = None
            else:
                _LOGGER.error("HTTP: %i - %s", resp.status_code, resp.text)
                result = None

        return result

    async def put(
        self, endpoint: str, body: dict, headers=None
    ) -> Union[dict, list, None]:
        """Make the request."""

        if self.token is None or self._has_expired(
            self.token_expiration, TOKEN_DURATION
        ):
            if await self.is_token_valid() is False:
                await self.get_new_token()

        if headers is None:
            headers = {}
        headers.update(
            {
                "Accept": "application/json, text/plain, */*",
                "Sec-Fetch-Dest": "empty",
                "X-TME-BRAND": "TOYOTA",
                "X-TME-LC": self.locale,
                "X-TME-TOKEN": self.token,
            }
        )

        async with httpx.AsyncClient() as client:
            resp = await client.put(
                endpoint, json=body, headers=headers, timeout=TIMEOUT
            )

            if resp.status_code == HTTP_OK:
                result = resp.json()
            elif resp.status_code == HTTP_NO_CONTENT:
                # This prevents raising or logging an error
                # if the user has not setup Connected Services
                result = None
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

    async def get_driving_statistics_endpoint(
        self, vin: str, from_date: str, interval: str = None
    ) -> dict:
        """Get driving statistic"""

        params = {"from": from_date, "calendarInterval": interval}

        return await self.get(
            f"{self.get_base_url()}/v2/trips/summarize", {"vin": vin}, params
        )
