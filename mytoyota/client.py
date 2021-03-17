"""Toyota Connected Services Client"""
import asyncio
import json
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
    ToyotaLocaleNotValid,
    ToyotaLoginError,
    ToyotaInvalidUsername,
    ToyotaRegionNotSupported,
)
from .utils import is_valid_locale, is_valid_uuid, is_valid_token

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Vehicle:
    """Object to hold car information for each car"""

    def __init__(  # pylint: disable=too-many-instance-attributes
        self,
        vehicle_info: Optional[dict],
        odometer: Optional[list],
        parking: Optional[dict],
        status: Optional[dict],
    ):
        self.odometer = None
        self.parking = None
        self.battery = None
        self.hvac = None
        self.alias = vehicle_info["alias"] if "alias" in vehicle_info else None
        self.vin = vehicle_info["vin"] if "vin" in vehicle_info else None
        self.details = {
            "hybrid": vehicle_info["hybrid"] if "hybrid" in vehicle_info else False,
            "model": vehicle_info["modelName"] if "modelName" in vehicle_info else None,
            "production_year": vehicle_info["productionYear"]
            if "productionYear" in vehicle_info
            else None,
            "fuel_type": vehicle_info["fuel"] if "fuel" in vehicle_info else None,
            "engine": vehicle_info["engine"] if "engine" in vehicle_info else None,
            "transmission": vehicle_info["transmission"]
            if "transmission" in vehicle_info
            else None,
            "image": vehicle_info["imageUrl"] if "imageUrl" in vehicle_info else None,
        }

        if not vehicle_info:
            _LOGGER.error("No vehicle information provided")
            return

        if not odometer:
            self.odometer = {"error": "Please setup Connected Services for your car"}
        else:
            instruments = {}
            for instrument in odometer:
                instruments[instrument["type"]] = instrument["value"]
                if "unit" in instrument:
                    instruments[instrument["type"] + "_unit"] = instrument["unit"]

            self.odometer = instruments

        if not parking:
            self.parking = {"error": "Please setup Connected Services for your car"}
        else:
            self.parking = parking

        if "VehicleInfo" in status:
            if "RemoteHvacInfo" in status["VehicleInfo"]:
                self.hvac = status["VehicleInfo"]["RemoteHvacInfo"]

            if "ChargeInfo" in status["VehicleInfo"]:
                self.battery = status["VehicleInfo"]["ChargeInfo"]
        else:
            self.battery = {"error": "Please setup Connected Services for your car"}
            self.hvac = {"error": "Please setup Connected Services for your car"}

    def __str__(self):
        return str(self.dict())

    def dict(self):
        """Return car information in dict"""
        return {
            "vin": self.vin,
            "alias": self.alias,
            "details": self.details,
            "status": {
                "hvac": self.hvac,
                "battery": self.battery,
                "odometer": self.odometer,
                "parking": self.parking,
            },
        }


class MyT:
    """Toyota Connected Services API class."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        locale: str,
        region: str,
        username: str = None,
        password: str = None,
        token: Optional[str] = None,
        uuid: Optional[str] = None,
    ) -> None:
        """Toyota API"""

        self.token = None
        self.uuid = None
        self.token_date: Optional[datetime] = None

        if region not in SUPPORTED_REGIONS:
            raise ToyotaRegionNotSupported(region)

        self.region = region

        if is_valid_locale(locale):
            self.locale = locale
        else:
            raise ToyotaLocaleNotValid(
                "Please provide a valid locale string! Valid format is: en-gb."
            )

        if token is not None and is_valid_token(token):
            self.token = token

        if uuid is not None and is_valid_uuid(uuid):
            self.uuid = uuid

        if "@" in username:
            self.username: str = username
        else:
            raise ToyotaInvalidUsername

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

    def get_uuid(self):
        """Get uuid string so you can reuse it."""
        return self.uuid

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
        """Performs login to toyota servers."""

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

    async def gather_information(self) -> list:
        """Gather all information, format it and return it as list"""
        vehicles = []
        cars = await self.get_vehicles_endpoint()
        if cars:
            for car in cars:
                vin = car["vin"]

                info = await asyncio.gather(
                    self.get_odometer_endpoint(vin),
                    self.get_parking_endpoint(vin),
                    self.get_vehicle_status_endpoint(vin),
                )

                vehicle = Vehicle(
                    vehicle_info=car, odometer=info[0], parking=info[1], status=info[2]
                )
                vehicles.append(vehicle.dict())

            return vehicles

    async def gather_information_json(self) -> str:
        """Gather all information, format it and return a json string"""
        vehicles = await self.gather_information()

        json_string = json.dumps(vehicles, indent=3)
        return json_string

    async def get(self, endpoint: str, headers=None):
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
            resp = await client.get(endpoint, headers=headers, timeout=TIMEOUT)

            if resp.status_code == HTTP_OK:
                result = resp.json()
            elif resp.status_code == HTTP_NO_CONTENT:
                result = None
            elif resp.status_code == HTTP_UNAUTHORIZED:
                self.invalidate_token()
                result = await self.get(endpoint, headers)
            else:
                _LOGGER.error("HTTP: %i - %s", resp.status_code, resp.text)
                result = None

            return result

    async def get_vehicles_endpoint(self) -> list:
        """Retrieves list of cars you have registered with MyT"""

        return await self.get(
            f"{self.get_base_url_cars()}/user/{self.uuid}/vehicles?services=uio&legacy=true"
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
