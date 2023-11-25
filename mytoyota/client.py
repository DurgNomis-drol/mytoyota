"""Client for connecting to Toyota Connected Services.

A client for connecting to MyT (Toyota Connected Services) and retrieving vehicle
information, sensor data, fuel level, driving statistics and more.

  Typical usage example:

  client = MyT()
  vehicles = await client.get_vehicles()
"""
from __future__ import annotations

import logging
from typing import Optional

from mytoyota.api import Api
from mytoyota.const import SUPPORTED_REGIONS
from mytoyota.models.vehicle import Vehicle

from .controller import Controller
from .exceptions import (
    ToyotaInvalidUsername,
    ToyotaLocaleNotValid,
    ToyotaRegionNotSupported,
)
from .utils.locale import is_valid_locale

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
        locale: str = "en-gb",
        region: str = "europe",
        brand: str = "T",
        uuid: Optional[str] = None,
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

        self._api = Api(
            controller_class(
                username=username,
                password=password,
                locale=locale,
                region=region,
                brand=brand,
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
        return list(SUPPORTED_REGIONS.keys())

    async def login(self) -> None:
        """Performs first login.

        Performs first login to Toyota's servers. Should be ideally be used
        the very first time you login in. Fetches a token and stores it in
        the controller object for future use.

        """
        _LOGGER.debug("Performing first login")
        await self._api.controller.first_login()

    async def get_vehicles(self) -> list[Vehicle]:
        """Returns a list of vehicles."""
        _LOGGER.debug("Getting list of vehicles associated with the account")
        vehicles = await self._api.get_vehicles_endpoint()

        return [Vehicle(self._api, v) for v in vehicles]

    # async def get_driving_statistics(  # pylint: disable=too-many-branches
    #     self,
    #     vin: str,
    #     interval: str = MONTH,
    #     from_date: str | None = None,
    #     unit: str = METRIC,
    # ) -> list[dict[str, Any]]:
    #     """Returns driving statistics from a given period.
    #
    #     Retrieves and formats driving statistics from a given period. Will return
    #     a error message on the first of each week, month or year. Or if no rides have been
    #     performed in the given period. This is due to a Toyota API limitation.
    #
    #     Args:
    #         vin (str):
    #             Vin number of vehicle you want statistics for.
    #         interval (str):
    #             Possible intervals are: "day", "week", "isoweek", "month" or "year".
    #             Defaults to "month" if none specified.
    #             Beware that "week" returns a week that starts on sunday and not monday.
    #             Use "isoweek" for a `normal` week. "isoweek" can only get data from
    #             the last/current week.
    #         from_date (str):
    #             Date-string format: "YYYY-MM-DD".
    #             Defaults to current day or the first of current week, month or year
    #             depending interval chosen.
    #         unit (str):
    #             Can be either: "metric", "imperial" OR "imperial_liters".
    #             Defaults to "metric".
    #
    #     Returns:
    #         A list of data points for the given period. Example response with interval "isoweek":
    #
    #         [
    #             {
    #                 "bucket": {
    #                     "year": "2021",
    #                     "week": "39",
    #                     "unit": "metric",
    #                     "periode_start": "2021-09-27"
    #                 },
    #                 "data": {
    #                     "tripCount": 17,
    #                     "totalDistanceInKm": 222.793,
    #                     "totalDurationInSec": 13893,
    #                     "idleDurationInSec": 852,
    #                     "highwayDistanceInKm": 66.206,
    #                     "nightTripsCount": 1,
    #                     "hardAccelerationCount": 23,
    #                     "hardBrakingCount": 12,
    #                     "averageSpeedInKmph": 57.730867,
    #                     "maxSpeedInKmph": 134.0,
    #                     "highwayDistancePercentage": 29.716373494678916
    #                 }
    #             }
    #         ]
    #
    #     Raises:
    #         ToyotaLoginError: An error returned when updating token or invalid login information.
    #         ToyotaInternalError: An error occurred when making a request.
    #         ToyotaApiError: Toyota's API returned an error.
    #     """
    #
    #     _LOGGER.debug(f"Getting statistics for {censor_vin(vin)}...")
    #     _LOGGER.debug(f"Interval: {interval} - from_date: {from_date} - unit: {unit}")
    #
    #     if interval not in INTERVAL_SUPPORTED:
    #         return [{"error_mesg": "Invalid interval provided!", "error_code": 1}]
    #
    #     stats_interval = interval
    #
    #     if from_date is not None and arrow.get(from_date) > arrow.now():
    #         return [{"error_mesg": "This is not a time machine!", "error_code": 5}]
    #
    #     if from_date is None:
    #         if interval is DAY:
    #             from_date = arrow.now().shift(days=-1).format(DATE_FORMAT)
    #
    #         if interval is WEEK:
    #             from_date = arrow.now().span(WEEK, week_start=7)[0].format(DATE_FORMAT)
    #
    #         if interval is ISOWEEK:
    #             stats_interval = DAY
    #             from_date = arrow.now().floor(WEEK).format(DATE_FORMAT)
    #
    #         if interval is MONTH:
    #             from_date = arrow.now().floor(MONTH).format(DATE_FORMAT)
    #
    #         if interval is YEAR:
    #             stats_interval = MONTH
    #             from_date = arrow.now().floor(YEAR).format(DATE_FORMAT)
    #
    #     if interval is ISOWEEK:
    #         stats_interval = DAY
    #         time_between = arrow.now() - arrow.get(from_date)
    #
    #         if time_between.days > 7:
    #             return [
    #                 {
    #                     "error_mesg": "Invalid date for isoweek provided! - from_date must not "
    #                     "be older then 7 days from now.",
    #                     "error_code": 3,
    #                 }
    #             ]
    #
    #         arrow.get(from_date).floor(WEEK).format(DATE_FORMAT)
    #
    #     if interval is YEAR:
    #         stats_interval = MONTH
    #
    #         if arrow.get(from_date) < arrow.now().floor(YEAR):
    #             return [
    #                 {
    #                     "error_mesg": "Invalid date provided. from_date can"
    #                     " only be current year. (" + interval + ")",
    #                     "error_code": 4,
    #                 }
    #             ]
    #
    #         from_date = arrow.get(from_date).floor(YEAR).format(DATE_FORMAT)
    #
    #     today = arrow.now().format(DATE_FORMAT)
    #
    #     if from_date == today:
    #         _LOGGER.debug(
    #             "Aborting getting statistics because day is on the first of the week,"
    #             " month or year"
    #         )
    #         raw_statistics = None
    #
    #     else:
    #         raw_statistics = await self.api.get_driving_statistics_endpoint(
    #             vin, from_date, stats_interval
    #         )
    #
    #     if raw_statistics is None:
    #         return [
    #             {
    #                 "error_mesg": "No data available for this period. ("
    #                 + interval
    #                 + ")",
    #                 "error_code": 2,
    #             }
    #         ]
    #
    #     # Format data so we get a uniform output.
    #
    #     imperial = False
    #     use_liters = False
    #
    #     if unit is IMPERIAL:
    #         imperial = True
    #     if unit is IMPERIAL_LITERS:
    #         imperial = True
    #         use_liters = True
    #
    #     _LOGGER.debug("Parse statistics into the statistics object for formatting...")
    #
    #     statistics = Statistics(
    #         raw_statistics=raw_statistics,
    #         interval=interval,
    #         imperial=imperial,
    #         use_liters=use_liters,
    #     )
    #
    #     return statistics.as_list()
    #
    # async def get_driving_statistics_json(
    #     self, vin: str, interval: str = MONTH, from_date: str | None = None
    # ) -> str:
    #     """Returns driving statistics from a given period as json.
    #
    #     Retrieves and formats driving statistics from a given period. Will return
    #     a error message on the first of each week, month or year. Or if no rides have been
    #     performed in the given period. This is due to a Toyota API limitation.
    #
    #     See get_driving_statistics() for args.
    #
    #     Returns:
    #         Pretty printed json string.
    #
    #     Raises:
    #         ToyotaLoginError: An error returned when updating token or invalid login information.
    #         ToyotaInternalError: An error occurred when making a request.
    #         ToyotaApiError: Toyota's API returned an error.
    #     """
    #     _LOGGER.debug("Returning it as json...")
    #     return json.dumps(
    #         await self.get_driving_statistics(vin, interval, from_date), indent=3
    #     )
    #
    # async def get_trips(self, vin: str) -> list[Trip]:
    #     """Returns a list of trips.
    #
    #     Retrieves and formats trips.
    #
    #     Args:
    #         vin (str):
    #             Vehicle identification number.
    #
    #     Returns:
    #         A list of trips.
    #
    #     Raises:
    #         ToyotaLoginError: An error returned when updating token or invalid login information.
    #         ToyotaInternalError: An error occurred when making a request.
    #         ToyotaApiError: Toyota's API returned an error.
    #     """
    #     _LOGGER.debug(f"Getting trips for {censor_vin(vin)}...")
    #
    #     raw_trips = await self.api.get_trips_endpoint(vin)
    #     _LOGGER.debug(f"received {len(raw_trips.get('recentTrips', []))} trips")
    #     return [Trip(trip) for trip in raw_trips.get("recentTrips", [])]
    #
    # async def get_trip(self, vin: str, trip_id: str) -> DetailedTrip:
    #     """Returns a trip.
    #
    #     Retrieves and formats a trip.
    #
    #     Args:
    #         vin (str):
    #             Vehicle identification number.
    #         trip_id (str):
    #             Trip id, UUID
    #
    #     Returns:
    #         A trip.
    #
    #     Raises:
    #         ToyotaLoginError: An error returned when updating token or invalid login information.
    #         ToyotaInternalError: An error occurred when making a request.
    #         ToyotaApiError: Toyota's API returned an error.
    #     """
    #     trip_id = trip_id.upper()
    #     _LOGGER.debug(f"Getting trip {trip_id} for {censor_vin(vin)}...")
    #
    #     raw_trip = await self.api.get_trip_endpoint(vin, trip_id)
    #     _LOGGER.debug(f"received trip {trip_id}")
    #     return DetailedTrip(raw_trip)
    #
    # async def get_trips_json(self, vin: str) -> str:
    #     """Returns a list of trips for a given vehicle.
    #
    #     Args:
    #         vin (str): Vehicle identification number.
    #
    #     Returns:
    #         A list of trips for the given vehicle.
    #
    #     Raises:
    #         ToyotaLoginError: An error returned when updating token or invalid login information.
    #         ToyotaInternalError: An error occurred when making a request.
    #         ToyotaApiError: Toyota's API returned an error.
    #     """
    #     trips = [trip.raw_json for trip in await self.get_trips(vin)]
    #     return json.dumps(trips, indent=3)
    #
    # async def get_trip_json(self, vin: str, trip_id: str) -> str:
    #     """Returns a trip for a given vehicle.
    #
    #     Args:
    #         vin (str): Vehicle identification number.
    #         trip_id (str): Trip id (UUID, Capitalized)
    #
    #     Returns:
    #         A Detailed Trip for the given vehicle.
    #
    #     Raises:
    #         ToyotaLoginError: An error returned when updating token or invalid login information.
    #         ToyotaInternalError: An error occurred when making a request.
    #         ToyotaApiError: Toyota's API returned an error.
    #     """
    #     trip = await self.get_trip(vin, trip_id)
    #     return json.dumps(trip.raw_json, indent=3)
    #
    # async def set_lock_vehicle(self, vin: str) -> VehicleLockUnlockActionResponse:
    #     """Sends a lock command to the vehicle.
    #
    #     Args:
    #         vin (str): Vehicle identification number.
    #
    #     Raises:
    #         ToyotaLoginError: An error returned when updating token or invalid login information.
    #         ToyotaActionNotSupported: The lock action is not supported on this vehicle.
    #         ToyotaInternalError: An error occurred when making a request.
    #         ToyotaApiError: Toyota's API returned an error.
    #     """
    #     _LOGGER.debug(f"Locking {censor_vin(vin)}...")
    #     raw_response = await self.api.set_lock_unlock_vehicle_endpoint(vin, "lock")
    #     _LOGGER.debug(f"Locking {censor_vin(vin)}... {raw_response}")
    #     response = VehicleLockUnlockActionResponse(raw_response)
    #     return response
    #
    # async def set_unlock_vehicle(self, vin: str) -> VehicleLockUnlockActionResponse:
    #     """Send an unlock command to the vehicle.
    #
    #     Args:
    #         vin (str): Vehicle identification number.
    #
    #     Raises:
    #         ToyotaLoginError: An error returned when updating token or invalid login information.
    #         ToyotaActionNotSupported: The lock action is not supported on this vehicle.
    #         ToyotaInternalError: An error occurred when making a request.
    #         ToyotaApiError: Toyota's API returned an error.
    #     """
    #     _LOGGER.debug(f"Unlocking {censor_vin(vin)}...")
    #     raw_response = await self.api.set_lock_unlock_vehicle_endpoint(vin, "unlock")
    #     _LOGGER.debug(f"Unlocking {censor_vin(vin)}... {raw_response}")
    #     response = VehicleLockUnlockActionResponse(raw_response)
    #     return response
    #
    # async def get_lock_status(
    #     self, vin: str, req_id: str
    # ) -> VehicleLockUnlockStatusResponse:
    #     """Get the status of a lock request.
    #
    #     Args:
    #         vin (str): Vehicle identification number.
    #         req_id (str): Lock/Unlock request id returned by
    #             set_<lock/unlock>_vehicle (UUID)
    #
    #     Raises:
    #         ToyotaLoginError: An error returned when updating token or invalid login information.
    #         ToyotaInternalError: An error occurred when making a request.
    #         ToyotaApiError: Toyota's API returned an error.
    #     """
    #     _LOGGER.debug(f"Getting lock request status for {censor_vin(vin)}...")
    #     raw_response = await self.api.get_lock_unlock_request_status(vin, req_id)
    #     _LOGGER.debug(
    #         f"Getting lock request status for {censor_vin(vin)}... {raw_response}"
    #     )
    #     response = VehicleLockUnlockStatusResponse(raw_response)
    #     return response
