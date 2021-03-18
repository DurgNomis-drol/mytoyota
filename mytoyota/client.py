"""Toyota Connected Services Client"""
import asyncio
import json
import logging

from .api import Controller
from .vehicle import Vehicle

from .const import (
    SUPPORTED_REGIONS,
)
from .exceptions import (
    ToyotaLocaleNotValid,
    ToyotaInvalidUsername,
    ToyotaRegionNotSupported,
)
from .utils import is_valid_locale

_LOGGER: logging.Logger = logging.getLogger(__package__)


class MyT:
    """Toyota Connected Services API class."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        username: str,
        password: str,
        locale: str,
        region: str,
    ) -> None:
        """Toyota API"""

        if "@" not in username:
            raise ToyotaInvalidUsername

        if region not in SUPPORTED_REGIONS:
            raise ToyotaRegionNotSupported(region)

        if not is_valid_locale(locale):
            raise ToyotaLocaleNotValid(
                "Please provide a valid locale string! Valid format is: en-gb."
            )

        self.api = Controller(
            locale=locale, region=region, username=username, password=password
        )

    async def login(self):
        """Login to Toyota services"""
        return await self.api.get_token()

    async def set_alias(self, vehicle_id: int, new_alias: str) -> dict:
        """Sets a new alias for the car"""
        result = await self.api.set_vehicle_alias_endpoint(
            vehicle_id=vehicle_id, new_alias=new_alias
        )
        return result

    async def get_vehicles(self) -> list:
        """Return list of vehicles with basic information about them"""

        cars = await self.api.get_vehicles_endpoint()
        if cars:
            return cars

    async def get_vehicles_json(self) -> str:
        """Return vehicle list as json"""
        vehicles = await self.get_vehicles()

        json_string = json.dumps(vehicles, indent=3)
        return json_string

    async def get_vehicle_information(self, vehicle: dict) -> dict:
        """Return information for given vehicle"""

        vin = vehicle["vin"]
        info = await asyncio.gather(
            self.api.get_connected_services_endpoint(vin),
            self.api.get_odometer_endpoint(vin),
            self.api.get_parking_endpoint(vin),
            self.api.get_vehicle_status_endpoint(vin),
        )

        car = Vehicle(
            vehicle_info=vehicle,
            connected_services=info[0],
            odometer=info[1],
            parking=info[2],
            status=info[3],
        )

        return car.as_dict()

    async def get_vehicle_information_json(self, vehicle: dict) -> str:
        """Return vehicle information as json"""
        vehicle = await self.get_vehicle_information(vehicle)

        json_string = json.dumps(vehicle, indent=3)
        return json_string

    async def gather_all_information(self) -> list:
        """Gather all information, format it and return it as list"""
        vehicles = []
        cars = await self.api.get_vehicles_endpoint()
        if cars:
            for car in cars:

                vehicle = await self.get_vehicle_information(car)

                vehicles.append(vehicle)

            return vehicles

    async def gather_all_information_json(self) -> str:
        """Gather all information, format it and return a json string"""
        vehicles = await self.gather_all_information()

        json_string = json.dumps(vehicles, indent=3)
        return json_string
