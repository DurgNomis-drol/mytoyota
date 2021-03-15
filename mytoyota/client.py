"""Toyota Connected Services Client"""
import asyncio
import logging
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
from .utils import is_valid_locale, is_valid_uuid, is_valid_token

# LOGGER
_LOGGER: logging.Logger = logging.getLogger(__package__)


class MyT:
    """Toyota Connected Services API class."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        locale: str,
        uuid: str = None,
        username: str = None,
        password: str = None,
        token: str = None,
    ) -> None:
        """Toyota API"""
        if is_valid_locale(locale):
            self._locale = locale
        else:
            raise ToyotaLocaleNotValid(
                "Please provide a valid locale string! Valid format is: en-gb."
            )

        self.username = username
        self.password = password
        self._token = token
        self._uuid = uuid

    def _request(self, endpoint: str, headers: dict):
        """Make the request."""

        result = None

        resp = requests.get(endpoint, headers=headers, timeout=TIMEOUT)

        if resp.status_code == HTTP_OK:
            result = resp.json()
        elif resp.status_code == 204:
            raise ToyotaNoCarError("Please setup connected services for your car!")
        elif resp.status_code == 401:
            token, uuid = self.perform_login(self.username, self.password)
            self._token = token
            self._uuid = uuid
        else:
            raise ToyotaHttpError("HTTP: {} - {}".format(resp.status_code, resp.text))

        return result

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

        if is_valid_uuid(uuid) and is_valid_token(token):
            self._uuid = uuid
            self._token = token

        return token, uuid

    async def get_information_for_given_car(self, vin):
        """Collects all information, validates it and then neatly formats it."""

        vehicle = await asyncio.gather(
            self._get_odometer_endpoint(vin),
            self._get_parking_endpoint(vin),
            self._get_vehicle_info_endpoint(vin),
        )

        return vehicle

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

        cars = self._request(endpoint, headers=headers)

        if isinstance(cars, list) and cars:
            return True, cars

        return False, None

    async def _get_odometer_endpoint(self, vin: str) -> tuple:
        """Get information from odometer."""

        print("Odometer...")

        odometer = 0
        odometer_unit = ""
        fuel = 0
        headers = {"Cookie": f"iPlanetDirectoryPro={self._token}"}
        endpoint = f"{BASE_URL}/vehicle/{vin}/addtionalInfo"

        retry, data = self._request(endpoint, headers=headers)

        if retry:
            retry, data = self._request(endpoint, headers=headers)

        for item in data:
            if item[TYPE] == MILEAGE:
                odometer = item[VALUE]
                odometer_unit = item[UNIT]
            if item[TYPE] == FUEL:
                fuel = item[VALUE]
        return odometer, odometer_unit, fuel

    async def _get_parking_endpoint(self, vin: str) -> tuple:
        """Get where you have parked your car."""
        print("Parking...")

        headers = {"Cookie": f"iPlanetDirectoryPro={self._token}", "VIN": vin}
        endpoint = f"{BASE_URL}/users/{self._uuid}/vehicle/location"

        parking = self._request(endpoint, headers=headers)

        return parking

    async def _get_vehicle_info_endpoint(self, vin: str) -> tuple:
        """Get information about the vehicle."""
        print("Vehicle...")
        headers = {
            "Cookie": f"iPlanetDirectoryPro={self._token}",
            "uuid": self._uuid,
            "X-TME-LOCALE": self._locale,
        }
        endpoint = f"{BASE_URL}/vehicles/{vin}/remoteControl/status"

        data = self._request(endpoint, headers=headers)

        last_updated = data[VEHICLE_INFO][ACQUISITIONDATE]
        battery = data[VEHICLE_INFO][CHARGE_INFO]
        hvac = data[VEHICLE_INFO][HVAC]

        return battery, hvac, last_updated
