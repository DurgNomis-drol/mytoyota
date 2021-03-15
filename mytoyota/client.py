"""Toyota Connected Services Client"""
import asyncio
import logging
from typing import Optional
from datetime import datetime
import requests


from .const import (
    BASE_URL,
    BASE_URL_CARS,
    CUSTOMERPROFILE,
    ENDPOINT_AUTH,
    HTTP_OK,
    PASSWORD,
    TIMEOUT,
    TOKEN,
    USERNAME,
    UUID,
    HTTP_NO_CONTENT,
    HTTP_UNAUTHORIZED,
    TOKEN_DURATION,
)
from .exceptions import (
    ToyotaHttpError,
    ToyotaLocaleNotValid,
    ToyotaLoginError,
    ToyotaNoCarError,
)
from .utils import is_valid_locale, is_valid_uuid, is_valid_token, odometer_list_to_dict

_LOGGER: logging.Logger = logging.getLogger(__package__)


class MyT:
    """Toyota Connected Services API class."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        locale: str,
        uuid: Optional[str] = None,
        username: str = None,
        password: str = None,
        token: Optional[str] = None,
    ) -> None:
        """Toyota API"""
        if is_valid_locale(locale):
            self._locale = locale
        else:
            raise ToyotaLocaleNotValid(
                "Please provide a valid locale string! Valid format is: en-gb."
            )

        self.username: str = username
        self.password: str = password
        self._token = token
        self._uuid = uuid
        self.token_date: Optional[datetime] = None

    @staticmethod
    def __token_has_expired(creation_dt, duration) -> bool:
        """Checks if token has expired."""
        return datetime.now().timestamp() - creation_dt.timestamp() > duration

    def invalidate_token(self):
        """Invalidates the current access token."""
        self._token = None
        self.token_date = None

    def api_get(self, endpoint: str, headers: dict):
        """Make the request."""

        resp = requests.get(endpoint, headers=headers, timeout=TIMEOUT)

        if resp.status_code == HTTP_OK:
            result = resp.json()
        elif resp.status_code == HTTP_NO_CONTENT:
            raise ToyotaNoCarError("Please setup connected services for your car!")
        elif resp.status_code == HTTP_UNAUTHORIZED:
            self.invalidate_token()
            return None
        else:
            raise ToyotaHttpError("HTTP: {} - {}".format(resp.status_code, resp.text))

        return result

    def get_token(self) -> tuple:
        """Performs login to toyota servers."""

        if self._token is None or self.__token_has_expired(
            self.token_date, TOKEN_DURATION
        ):

            headers = {
                "X-TME-BRAND": "TOYOTA",
                "X-TME-LC": self._locale,
                "Accept": "application/json, text/plain, */*",
                "Sec-Fetch-Dest": "empty",
                "Content-Type": "application/json;charset=UTF-8",
            }

            # Cannot authenticate with aiohttp (returns 415),
            # but it works with requests.
            response = requests.post(
                ENDPOINT_AUTH,
                headers=headers,
                json={USERNAME: self.username, PASSWORD: self.password},
            )
            if response.status_code == HTTP_OK:
                result = response.json()

                token = result.get(TOKEN)
                uuid = result[CUSTOMERPROFILE][UUID]

                if is_valid_token(token) and is_valid_uuid(uuid):
                    self._uuid = uuid
                    self._token = token
                    self.token_date = datetime.now()
                    return token, uuid

            raise ToyotaLoginError(
                "Login failed, check your credentials! {}".format(response.text)
            )

        return None, None

    async def get_vehicle_status(self, vin) -> dict:
        """Collects all information, validates it and then neatly formats it."""
        info = await asyncio.gather(
            self.__get_odometer_endpoint(vin),
            self.__get_parking_endpoint(vin),
            self.__get_vehicle_status_endpoint(vin),
        )

        vehicle = {
            "odometer": odometer_list_to_dict(info[0]) if info[0] is not None else None,
            "parking": info[1],
            "status": info[2],
        }

        return vehicle

    async def get_vehicles(self) -> dict:
        """Retrieves list of cars you have registered with MyT"""
        headers = {
            "X-TME-BRAND": "TOYOTA",
            "X-TME-LC": self._locale,
            "Accept": "application/json, text/plain, */*",
            "Sec-Fetch-Dest": "empty",
            "X-TME-TOKEN": self._token,
        }

        endpoint = (
            f"{BASE_URL_CARS}/user/{self._uuid}/vehicles?services=uio&legacy=true"
        )

        cars = self.api_get(endpoint, headers=headers)

        return cars

    async def __get_odometer_endpoint(self, vin: str) -> dict:
        """Get information from odometer."""
        headers = {"Cookie": f"iPlanetDirectoryPro={self._token}"}
        endpoint = f"{BASE_URL}/vehicle/{vin}/addtionalInfo"

        odometer = self.api_get(endpoint, headers=headers)

        return odometer

    async def __get_parking_endpoint(self, vin: str) -> dict:
        """Get where you have parked your car."""
        headers = {"Cookie": f"iPlanetDirectoryPro={self._token}", "VIN": vin}
        endpoint = f"{BASE_URL}/users/{self._uuid}/vehicle/location"

        parking = self.api_get(endpoint, headers=headers)

        return parking

    async def __get_vehicle_status_endpoint(self, vin: str) -> dict:
        """Get information about the vehicle."""
        headers = {
            "Cookie": f"iPlanetDirectoryPro={self._token}",
            "uuid": self._uuid,
            "X-TME-LOCALE": self._locale,
        }
        endpoint = f"{BASE_URL}/vehicles/{vin}/remoteControl/status"

        status = self.api_get(endpoint, headers=headers)

        return status
