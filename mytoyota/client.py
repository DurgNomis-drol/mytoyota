"""Toyota Connected Services Client"""
import logging

import aiohttp
import requests

from .const import (
    ACQUISITIONDATE,
    BASE_URL,
    BASE_URL_CARS,
    CHARGE_INFO,
    CUSTOMERPROFILE,
    ENDPOINT_AUTH,
    FUEL,
    HTTP_OK,
    HVAC,
    MILEAGE,
    PASSWORD,
    TIMEOUT,
    TOKEN,
    TYPE,
    UNIT,
    USERNAME,
    UUID,
    VALUE,
    VEHICLE_INFO,
)
from .exceptions import (
    ToyotaHttpError,
    ToyotaLocaleNotValid,
    ToyotaLoginError,
    ToyotaNoCarError,
)
from .utils import locale_is_valid

# LOGGER
_LOGGER: logging.Logger = logging.getLogger(__package__)


class MyT:
    """Toyota Connected Services API class."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        locale: str,
        session: aiohttp.ClientSession,
        uuid: str = None,
        username: str = None,
        password: str = None,
        token: str = None,
    ) -> None:
        """Toyota API"""
        if locale_is_valid(locale):
            self._locale = locale
        else:
            raise ToyotaLocaleNotValid(
                "Please provide a valid locale string! Valid format is: en-gb."
            )

        self.session = session
        self.username = username
        self.password = password
        self._token = token
        self._uuid = uuid

    async def _request(self, endpoint: str, headers: dict) -> tuple:
        """Make the request."""

        resp = None
        async with self.session.get(
            endpoint, headers=headers, timeout=TIMEOUT
        ) as response:
            if response.status == HTTP_OK:
                resp = await response.json()
            elif response.status == 204:
                # If you have not enabled connected services.
                raise ToyotaNoCarError("Please setup connected services for your car!")
            elif response.status == 401:
                # If the token has expired.
                token, uuid = self.perform_login(self.username, self.password)
                self._token = token
                self._uuid = uuid
                return False, None
            else:
                raise ToyotaHttpError(
                    "HTTP: {} - {}".format(response.status, response.text)
                )

        return True, resp

    def perform_login(self, username: str, password: str) -> tuple:
        """Performs login to toyota servers."""
        headers = {
            "X-TME-BRAND": "TOYOTA",
            "X-TME-LC": self._locale,
            "Accept": "application/json, text/plain, */*",
            "Sec-Fetch-Dest": "empty",
            "Content-Type": "application/json;charset=UTF-8",
        }

        # Cannot authenticate with aiohttp (returns 415), but it works with requests.
        response = requests.post(
            ENDPOINT_AUTH,
            headers=headers,
            json={USERNAME: username, PASSWORD: password},
        )
        if response.status_code != HTTP_OK:
            raise ToyotaLoginError(
                "Login failed, check your credentials! {}".format(response.text)
            )

        result = response.json()

        token = result.get(TOKEN)
        uuid = result[CUSTOMERPROFILE][UUID]

        self._token = token
        self._uuid = uuid

        return token, uuid

    async def get_cars(self) -> tuple:
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

        retry, cars = await self._request(endpoint, headers=headers)

        if retry:
            retry, cars = await self._request(endpoint, headers=headers)

        if isinstance(cars, list) and cars:
            return True, cars

        return False, None

    async def get_odometer(self, vin: str) -> tuple:
        """Get information from odometer."""
        odometer = 0
        odometer_unit = ""
        fuel = 0
        headers = {"Cookie": f"iPlanetDirectoryPro={self._token}"}
        endpoint = f"{BASE_URL}/vehicle/{vin}/addtionalInfo"

        retry, data = await self._request(endpoint, headers=headers)

        if retry:
            retry, data = await self._request(endpoint, headers=headers)

        for item in data:
            if item[TYPE] == MILEAGE:
                odometer = item[VALUE]
                odometer_unit = item[UNIT]
            if item[TYPE] == FUEL:
                fuel = item[VALUE]
        return odometer, odometer_unit, fuel

    async def get_parking(self, vin: str) -> dict:
        """Get where you have parked your car."""
        headers = {"Cookie": f"iPlanetDirectoryPro={self._token}", "VIN": vin}
        endpoint = f"{BASE_URL}/users/{self._uuid}/vehicle/location"

        retry, parking = await self._request(endpoint, headers=headers)

        if retry:
            retry, parking = await self._request(endpoint, headers=headers)

        return parking

    async def get_vehicle_information(self, vin: str) -> tuple:
        """Get information about the vehicle."""
        headers = {
            "Cookie": f"iPlanetDirectoryPro={self._token}",
            "uuid": self._uuid,
            "X-TME-LOCALE": self._locale,
        }
        endpoint = f"{BASE_URL}/vehicles/{vin}/remoteControl/status"

        retry, data = await self._request(endpoint, headers=headers)

        if retry:
            retry, data = await self._request(endpoint, headers=headers)

        last_updated = data[VEHICLE_INFO][ACQUISITIONDATE]
        battery = data[VEHICLE_INFO][CHARGE_INFO]
        hvac = data[VEHICLE_INFO][HVAC]

        return battery, hvac, last_updated
