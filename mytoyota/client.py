"""Client for connecting to Toyota Connected Services.

A client for connecting to MyT (Toyota Connected Services) and retrieving vehicle
information, sensor data, fuel level, driving statistics and more.

  Typical usage example:

  client = MyT()
  vehicles = await client.get_vehicles()
"""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

import arrow

from .api import Api
from .const import (
    DATE_FORMAT,
    DAY,
    IMPERIAL,
    IMPERIAL_LITERS,
    INTERVAL_SUPPORTED,
    ISOWEEK,
    METRIC,
    MONTH,
    SUPPORTED_REGIONS,
    WEEK,
    YEAR,
)
from .controller import Controller
from .exceptions import (
    ToyotaInvalidUsername,
    ToyotaLocaleNotValid,
    ToyotaRegionNotSupported,
)
from .models.vehicle import Vehicle
from .statistics import Statistics
from .utils.locale import is_valid_locale
from .utils.logs import censor, censor_vin

_LOGGER: logging.Logger = logging.getLogger(__package__)


class MyT:
    """Toyota Connected Services client.

    Toyota connected services client class. This is the class that you
    should interact with when using this library.
    """

    def __init__(
        self,
        username: str,
        password: str,
        locale: str = "da-dk",
        region: str = "europe",
        uuid: str = None,
        controller_class=Controller,
        disable_locale_check: bool = False,
    ) -> None:
        """Toyota API"""

        if username is None or "@" not in username:
            raise ToyotaInvalidUsername

        if region not in SUPPORTED_REGIONS:
            raise ToyotaRegionNotSupported(region)

        if not disable_locale_check:
            if not is_valid_locale(locale):
                raise ToyotaLocaleNotValid(
                    "Please provide a valid locale string! Valid format is: en-gb."
                )

        self.api = Api(
            controller_class(
                username=username,
                password=password,
                locale=locale,
                region=region,
                uuid=uuid,
            )
        )

    @staticmethod
    def get_supported_regions() -> list:
        """Get supported regions.

        Retrieves a list of supported regions.

        Returns:
            A list of supported regions. For example: ["europe"]
        """
        regions = []

        for key, _ in SUPPORTED_REGIONS.items():  # pylint: disable=unused-variable
            regions.append(key)

        return regions

    async def login(self) -> None:
        """Performs first login.

        Performs first login to Toyota's servers. Should be ideally be used
        the very first time you login in. Fetches a token and stores it in
        the controller object for future use.

        """
        _LOGGER.debug("Performing first login")
        await self.api.controller.first_login()

    @property
    def uuid(self) -> str | None:
        """Get UUID.

        Retrieves the UUID returned for the account.

        Returns:
            UUIDv4 unique ID for the logged in account. Example:

            9cc70412-27d6-4b81-83fb-542b3a9feb65
        """
        return self.api.uuid

    async def set_alias(self, vehicle_id: int, new_alias: str) -> dict[str, Any]:
        """Set a new alias for your vehicle.

        Sets a new alias for a vehicle specified by its vehicle id.

        Args:
            vehicle_id (int): Vehicle id is a 7 digit number identifying your vehicle.
            new_alias (str): New alias of the vehicle.

        Returns:
            Returns a dict containing the changed alias and the vehicle id. Example:

            {"id":"2199911","alias":"lightning mcqueen"}

        Raises:
            ToyotaLoginError: An error returned when updating token or invalid login information.
            ToyotaInternalError: An error occurred when making a request.
            ToyotaApiError: Toyota's API returned an error.
        """
        _LOGGER.debug(
            f"Setting new alias: {new_alias} for vehicle with id: {censor(str(vehicle_id))}"
        )
        return await self.api.set_vehicle_alias_endpoint(
            vehicle_id=vehicle_id, new_alias=new_alias
        )

    async def get_vehicles(self) -> list[dict[str, Any]]:
        """Returns a list of vehicles.

        Retrieves list of vehicles associated with the account. The list contains static
        information about the vehicle, numberplate and starter battery health.

        Returns:
            Returns a list containing mostly static information about a vehicle. Example:

            [
               {
                  "id":1111111,
                  "vin":"XXXXGNEC00NXXXXXX",
                  "isNC":true,
                  "batteryHealth":"GOOD",
                  "alias":"Aygo",
                  "owner":true,
                  "claimedBy":"MT-EHUB",
                  "startDate":"2021-03-19T09:20:42.152Z",
                  "vehicleAddedOn":"2021-03-12T09:43:42.350Z",
                  "isEntitled":true,
                  "entitledBy":"MT-EHUB",
                  "entitledOn":"2021-03-19T09:20:42.152Z",
                  "ownerFlag":true,
                  "source":"NMSC",
                  "horsePower":72,
                  "hybrid":false,
                  "fuel":"1.0P",
                  "engine":"1.0P",
                  "transmissionType":"MT",
                  "transmission":"5 M/T",
                  "grade":"Mid/High",
                  "modelName":"Aygo 2B",
                  "modelCode":"AY",
                  "interiorColour":"20",
                  "exteriorColour":"1E0 ",
                  "imageUrl":"https://dj3z27z47basa.cloudfront.net/5957a713-f80f-483f-998c-97f956367048",  # pylint: disable=line-too-long
                  "modelDocumentId":"12345",
                  "productionYear":"2021",
                  "licensePlate":"XX11111",
                  "modelDescription":"Aygo 2B"
               }
            ]

        Raises:
            ToyotaLoginError: An error returned when updating token or invalid login information.
            ToyotaInternalError: An error occurred when making a request.
            ToyotaApiError: Toyota's API returned an error.
        """
        _LOGGER.debug("Getting list of vehicles associated with the account")
        vehicles = await self.api.get_vehicles_endpoint()
        if vehicles:
            return vehicles

    async def get_vehicles_json(self) -> str:
        """Returns a list of vehicles as json string.

        Retrieves list of vehicles associated with the account. The list contains static
        information about the vehicle, numberplate and starter battery health.
        Returns it as a json string.

        Returns:
            See get_vehicles() for an example of what this function returns.

        Raises:
            ToyotaLoginError: An error returned when updating token or invalid login information.
            ToyotaInternalError: An error occurred when making a request.
            ToyotaApiError: Toyota's API returned an error.
        """
        vehicles = await self.get_vehicles()

        _LOGGER.debug("Returning it as json...")
        return json.dumps(vehicles, indent=3)

    async def get_vehicle_status(self, vehicle: dict[str, Any]) -> Vehicle:
        """Returns vehicle status.

        Collects and formats different vehicle status endpoints into
        a easy accessible vehicle object.

        Args:
            vehicle (dict): dict for each vehicle returned in get_vehicles().

        Returns:
            Vehicle object containing odometer information, parking information, fuel and more.

        Raises:
            ToyotaLoginError: An error returned when updating token or invalid login information.
            ToyotaInternalError: An error occurred when making a request.
            ToyotaApiError: Toyota's API returned an error.
        """
        vin = vehicle.get("vin")
        _LOGGER.debug(f"Getting status for vehicle - {censor_vin(vin)}...")

        data = await asyncio.gather(
            *[
                self.api.get_connected_services_endpoint(vin),
                self.api.get_odometer_endpoint(vin),
                self.api.get_vehicle_status_endpoint(vin),
                self.api.get_vehicle_status_legacy_endpoint(vin),
            ]
        )

        _LOGGER.debug("Presenting information as an object...")

        return Vehicle(
            vehicle_info=vehicle,
            connected_services=data[0],
            odometer=data[1],
            status=data[2],
            status_legacy=data[3],
        )

    async def get_driving_statistics(  # pylint: disable=too-many-branches
        self,
        vin: str,
        interval: str = MONTH,
        from_date: str | None = None,
        unit: str = METRIC,
    ) -> list[dict[str, Any]]:
        """Returns driving statistics from a given period.

        Retrieves and formats driving statistics from a given periode. Will return
        a error message on the first of each week, month or year. Or if no rides have been
        performed in the given periode. This is due to a Toyota API limitation.

        Args:
            vin (str):
                Vin number of vehicle you want statistics for.
            interval (str):
                Possible intervals are: "day", "week", "isoweek", "month" or "year".
                Defaults to "month" if none specified.
                Beware that "week" returns a week that starts on sunday and not monday.
                Use "isoweek" for a `normal` week. "isoweek" can only get data from
                the last/current week.
            from_date (str):
                Date-string format: "YYYY-MM-DD".
                Defaults to current day or the first of current week, month or year
                depending interval chosen.
            unit (str):
                Can be either: "metric", "imperial" OR "imperial_liters".
                Defaults to "metric".

        Returns:
            A list of data points for the given periode. Example response with interval "isoweek":

            [
                {
                    "bucket": {
                        "year": "2021",
                        "week": "39",
                        "unit": "metric",
                        "periode_start": "2021-09-27"
                    },
                    "data": {
                        "tripCount": 17,
                        "totalDistanceInKm": 222.793,
                        "totalDurationInSec": 13893,
                        "idleDurationInSec": 852,
                        "highwayDistanceInKm": 66.206,
                        "nightTripsCount": 1,
                        "hardAccelerationCount": 23,
                        "hardBrakingCount": 12,
                        "averageSpeedInKmph": 57.730867,
                        "maxSpeedInKmph": 134.0,
                        "highwayDistancePercentage": 29.716373494678916
                    }
                }
            ]

        Raises:
            ToyotaLoginError: An error returned when updating token or invalid login information.
            ToyotaInternalError: An error occurred when making a request.
            ToyotaApiError: Toyota's API returned an error.
        """

        _LOGGER.debug(f"Getting statistics for {censor_vin(vin)}...")
        _LOGGER.debug(f"Interval: {interval} - from_date: {from_date} - unit: {unit}")

        if interval not in INTERVAL_SUPPORTED:
            return [{"error_mesg": "Invalid interval provided!", "error_code": 1}]

        stats_interval = interval

        if from_date is not None and arrow.get(from_date) > arrow.now():
            return [{"error_mesg": "This is not a time machine!", "error_code": 5}]

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
            _LOGGER.debug(
                "Aborting getting statistics because day is on the first of the week,"
                " month or year"
            )
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

        imperial = False
        use_liters = False

        if unit is IMPERIAL:
            imperial = True
        if unit is IMPERIAL_LITERS:
            imperial = True
            use_liters = True

        _LOGGER.debug("Parse statistics into the statistics object for formatting...")

        statistics = Statistics(
            raw_statistics=raw_statistics,
            interval=interval,
            imperial=imperial,
            use_liters=use_liters,
        )

        return statistics.as_list()

    async def get_driving_statistics_json(
        self, vin: str, interval: str = MONTH, from_date: str | None = None
    ) -> str:
        """Returns driving statistics from a given period as json.

        Retrieves and formats driving statistics from a given periode. Will return
        a error message on the first of each week, month or year. Or if no rides have been
        performed in the given periode. This is due to a Toyota API limitation.

        See get_driving_statistics() for args.

        Returns:
            Pretty printed json string.

        Raises:
            ToyotaLoginError: An error returned when updating token or invalid login information.
            ToyotaInternalError: An error occurred when making a request.
            ToyotaApiError: Toyota's API returned an error.
        """
        _LOGGER.debug("Returning it as json...")
        return json.dumps(
            await self.get_driving_statistics(vin, interval, from_date), indent=3
        )
