"""Toyota Connected Services Client"""
import asyncio
import json
import logging

import arrow

from .api import Controller
from .const import (
    SUPPORTED_REGIONS,
)
from .exceptions import (
    ToyotaLocaleNotValid,
    ToyotaInvalidUsername,
    ToyotaRegionNotSupported,
)
from .utils import is_valid_locale
from .vehicle import Vehicle

_LOGGER: logging.Logger = logging.getLogger(__package__)


class MyT:
    """Toyota Connected Services API class."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        username: str,
        password: str,
        locale: str,
        region: str,
        uuid: str = None,
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
            locale=locale,
            region=region,
            username=username,
            password=password,
            uuid=uuid,
        )

    @staticmethod
    def get_supported_regions():
        """Return supported regions"""
        regions = []

        for key, value in SUPPORTED_REGIONS.items():  # pylint: disable=unused-variable
            regions.append(key)

        return regions

    async def login(self) -> None:
        """Login to Toyota services"""
        await self.api.get_new_token()

    async def get_uuid(self) -> str:
        """Get uuid"""
        return await self.api.get_uuid()

    async def set_alias(self, vehicle_id: int, new_alias: str) -> dict:
        """Sets a new alias for the car"""
        result = await self.api.set_vehicle_alias_endpoint(
            vehicle_id=vehicle_id, new_alias=new_alias
        )
        return result

    async def get_vehicles(self) -> list:
        """Return list of vehicles with basic information about them"""

        vehicles = await self.api.get_vehicles_endpoint()
        if vehicles:
            return vehicles

    async def get_vehicles_json(self) -> str:
        """Return vehicle list as json"""
        vehicles = await self.get_vehicles()

        json_string = json.dumps(vehicles, indent=3)
        return json_string

    async def get_vehicle_status(self, vehicle: dict) -> dict:
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

    async def get_vehicle_status_json(self, vehicle: dict) -> str:
        """Return vehicle information as json"""
        vehicle = await self.get_vehicle_status(vehicle)

        json_string = json.dumps(vehicle, indent=3)
        return json_string

    async def get_driving_statistics(
        self, vin: str, interval: str = "month", from_date=None
    ) -> dict:
        """
        params: vin: Vin number of your car.
                interval: can be "day", "week" or "month". Default "month"
                from_date: from which date you want statistics. Default is current day,
                week or month if None.

                Week numbers are not ISO week numbers, but Japan week numbers.

                A week starts on a Sunday and not Monday.

                Will return null if no ride have been performed in the timeframe.
        """

        if interval not in ("day", "week", "month"):
            return {"Error_mesg": "Invalid interval provided!"}

        def calculate_from_date() -> str:
            if interval == "day":
                date = arrow.now().shift(days=-1).format("YYYY-MM-DD")
                return date

            if interval == "week":
                date = arrow.now().span("week", week_start=7)[0].format("YYYY-MM-DD")

                if date == arrow.now().format("YYYY-MM-DD"):
                    date = (
                        arrow.now()
                        .span("week", week_start=7)[0]
                        .shift(days=-1)
                        .format("YYYY-MM-DD")
                    )
                return date

            date = arrow.now().floor("month").format("YYYY-MM-DD")

            if date == arrow.now().format("YYYY-MM_DD"):
                date = (
                    arrow.now()
                    .span("month", week_start=7)[0]
                    .shift(days=-1)
                    .format("YYYY-MM-DD")
                )
            return date

        if from_date is None:
            from_date = calculate_from_date()

        statistics = await self.api.get_driving_statistics_endpoint(
            vin, from_date, interval
        )

        return statistics

    async def get_driving_statistics_json(
        self, vin: str, interval: str = "month", from_date=None
    ) -> str:
        """Return driving statistics in json"""
        return json.dumps(
            await self.get_driving_statistics(vin, interval, from_date), indent=3
        )
