"""Toyota Connected Services Client"""
import asyncio
import json
import logging

import arrow

from .api import Controller
from .const import (
    DATE_FORMAT,
    DAY,
    INTERVAL_SUPPORTED,
    ISOWEEK,
    MONTH,
    SUPPORTED_REGIONS,
    WEEK,
    YEAR,
)
from .exceptions import (
    ToyotaInvalidUsername,
    ToyotaLocaleNotValid,
    ToyotaRegionNotSupported,
)
from .statistics import Statistics
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
    def get_supported_regions() -> list:
        """Return supported regions"""
        regions = []

        for key, _ in SUPPORTED_REGIONS.items():  # pylint: disable=unused-variable
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

    async def get_vehicle_status(self, vehicle: dict) -> Vehicle:
        """Return information for given vehicle"""

        vin = vehicle["vin"]
        info = await asyncio.gather(
            *[
                self.api.get_connected_services_endpoint(vin),
                self.api.get_odometer_endpoint(vin),
                self.api.get_vehicle_status_endpoint(vin),
            ]
        )

        car = Vehicle(
            vehicle_info=vehicle,
            connected_services=info[0],
            odometer=info[1],
            status=info[2],
        )

        return car

    async def get_vehicle_status_json(self, vehicle: dict) -> str:
        """Return vehicle information as json"""
        vehicle = await self.get_vehicle_status(vehicle)

        json_string = json.dumps(vehicle.as_dict(), indent=3)
        return json_string

    async def get_driving_statistics(  # pylint: disable=too-many-branches
        self, vin: str, interval: str = MONTH, from_date: str = None
    ) -> list:
        """
        params: vin: Vin number of your car.
                interval: can be "day", "week", "isoweek", "month" or "year". Default "month"
                from_date: from which date you want statistics. Default is current day,
                week or month if None.

                "day" will return yesterday

                "week" uses Japan weeknumbers and not ISOweeknumbers.

                Use "isoweek" if you want Monday to Sunday. "week" returns Sunday to Saturday.

                Will return a error message if no ride have been performed in the timeframe
                or no data is available yet.

                On the first of each week, month or year. This will return an error message.
                This is due to a Toyota API limitation.
        """

        if interval not in INTERVAL_SUPPORTED:
            return [{"error_mesg": "Invalid interval provided!", "error_code": 1}]

        stats_interval = interval

        if from_date is not None and arrow.get(from_date) > arrow.now():
            return [{"error_mesg": "This is not a timemachine!", "error_code": 5}]

        if from_date is None:
            if interval is DAY:
                from_date = arrow.now().shift(days=-1).format(DATE_FORMAT)

            if interval is WEEK:
                from_date = arrow.now().span(WEEK, week_start=7)[0].format(DATE_FORMAT)

            if interval is ISOWEEK:
                stats_interval = DAY
                from_date = arrow.now().floor(WEEK).format(DATE_FORMAT)

            if interval is MONTH:
                from_date = arrow.now().floor(MONTH).format(DATE_FORMAT)

            if interval is YEAR:
                stats_interval = MONTH
                from_date = arrow.now().floor(YEAR).format(DATE_FORMAT)

        if interval is ISOWEEK:
            stats_interval = DAY
            time_between = arrow.now() - arrow.get(from_date)

            if time_between.days > 7:
                return [
                    {
                        "error_mesg": "Invalid date for isoweek provided! - from_date must not "
                        "be older then 7 days from now.",
                        "error_code": 3,
                    }
                ]

            arrow.get(from_date).floor(WEEK).format(DATE_FORMAT)

        if interval is YEAR:
            stats_interval = MONTH

            if arrow.get(from_date) < arrow.now().floor(YEAR):
                return [
                    {
                        "error_mesg": "Invalid date provided. from_date can"
                        " only be current year. (" + interval + ")",
                        "error_code": 4,
                    }
                ]

            from_date = arrow.get(from_date).floor(YEAR).format(DATE_FORMAT)

        today = arrow.now().format(DATE_FORMAT)

        if from_date == today:
            raw_statistics = None

        else:
            raw_statistics = await self.api.get_driving_statistics_endpoint(
                vin, from_date, stats_interval
            )

        if raw_statistics is None:
            return [
                {
                    "error_mesg": "No data available for this period. ("
                    + interval
                    + ")",
                    "error_code": 2,
                }
            ]

        # Format data so we get a uniform output.
        statistics = Statistics(raw_statistics, interval)

        return statistics.as_list()

    async def get_driving_statistics_json(
        self, vin: str, interval: str = MONTH, from_date: str = None
    ) -> str:
        """Return driving statistics in json"""
        return json.dumps(
            await self.get_driving_statistics(vin, interval, from_date), indent=3
        )
