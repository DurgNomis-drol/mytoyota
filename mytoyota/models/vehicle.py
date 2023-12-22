"""Vehicle model."""
import asyncio
import calendar
import copy
from datetime import date, timedelta
from functools import partial
import json
import logging
from typing import Any, Dict, List, Optional, Tuple

from mytoyota.api import Api
from mytoyota.models.dashboard import Dashboard
from mytoyota.models.endpoints.vehicle_guid import VehicleGuidModel
from mytoyota.models.location import Location
from mytoyota.models.lock_status import LockStatus
from mytoyota.models.nofication import Notification
from mytoyota.models.summary import Summary, SummaryType
from mytoyota.models.trips import Trip
from mytoyota.utils.logs import censor_all

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Vehicle:
    """Vehicle data representation."""

    def __init__(
        self, api: Api, vehicle_info: VehicleGuidModel, metric: bool = True
    ) -> None:
        """Initialise the Vehicle data representation."""
        self._vehicle_info = vehicle_info
        self._api = api
        self._endpoint_data: Dict[str, Any] = {}
        self._metric = metric

        # Endpoint Name, Function to check if car supports the endpoint, endpoint to call to update
        api_endpoints = [
            {
                "name": "location",
                "capable": vehicle_info.extended_capabilities.last_parked_capable
                or vehicle_info.features.last_parked,
                "function": partial(
                    self._api.get_location_endpoint, vin=vehicle_info.vin
                ),
            },
            {
                "name": "health_status",
                "capable": True,  # TODO Unsure of the required capability # pylint: disable=W0511
                "function": partial(
                    self._api.get_vehicle_health_status_endpoint,
                    vin=vehicle_info.vin,
                ),
            },
            {
                "name": "electric_status",
                "capable": vehicle_info.extended_capabilities.econnect_vehicle_status_capable,
                "function": partial(
                    self._api.get_vehicle_electric_status_endpoint,
                    vin=vehicle_info.vin,
                ),
            },
            {
                "name": "telemetry",
                "capable": vehicle_info.extended_capabilities.telemetry_capable,
                "function": partial(
                    self._api.get_telemetry_endpoint, vin=vehicle_info.vin
                ),
            },
            {
                "name": "notifications",
                "capable": True,  # TODO Unsure of the required capability # pylint: disable=W0511
                "function": partial(
                    self._api.get_notification_endpoint, vin=vehicle_info.vin
                ),
            },
            {
                "name": "status",
                "capable": vehicle_info.extended_capabilities.vehicle_status,
                "function": partial(
                    self._api.get_remote_status_endpoint, vin=vehicle_info.vin
                ),
            },
            {
                "name": "trips",
                "capable": True,  # TODO Unsure of the required capability # pylint: disable=W0511
                "function": partial(
                    self._api.get_trips_endpoint,
                    vin=vehicle_info.vin,
                    from_date=date.today() - timedelta(days=1),
                    to_date=date.today(),
                ),
            },
        ]
        self._endpoint_collect = [
            (endpoint["name"], endpoint["function"])
            for endpoint in api_endpoints
            if endpoint["capable"]
        ]

    async def update(self) -> None:
        """Update the data for the vehicle.

        This method asynchronously updates the data for the vehicle by
        calling the endpoint functions in parallel.

        Returns
        -------
            None

        """

        async def parallel_wrapper(
            name: str, function: partial
        ) -> Tuple[str, Dict[str, Any]]:
            r = await function()
            return name, r

        responses = asyncio.gather(
            *[
                parallel_wrapper(name, function)
                for name, function in self._endpoint_collect
            ]
        )
        for name, data in await responses:
            self._endpoint_data[name] = data

    @property
    def vin(self) -> Optional[str]:
        """Return the vehicles VIN number.

        Returns
        -------
            The vehicles VIN number

        """
        return self._vehicle_info.vin

    @property
    def alias(self) -> Optional[str]:
        """Vehicle's alias.

        Returns
        -------
            Nickname of vehicle

        """
        return self._vehicle_info.nickname

    @property
    def type(self) -> Optional[str]:
        """Returns the "type" of vehicle.

        Returns
        -------
            "fuel" if only fuel based
            "mildhybrid" if hybrid
            "phev" if plugin hybrid
            "ev" if full electric vehicle
        """
        # TODO enum # pylint: disable=W0511
        # TODO currently guessing until we see a mild hybrid and full EV # pylint: disable=W0511
        # TODO should probably use electricalPlatformCode but values currently unknown # pylint: disable=W0511
        # TODO list of fuel types. ?: G=Petrol Only, I=Hybrid # pylint: disable=W0511
        return (
            "phev"
            if self._vehicle_info.ev_vehicle and self._vehicle_info.fuel_type
            else "ev"
        )

    @property
    def dashboard(self) -> Optional[Dashboard]:
        """Returns the Vehicle dashboard.

        The dashboard consists of items of information you would expect to
        find on the dashboard. i.e. Fuel Levels.

        Returns
        -------
            A dashboard
        """
        # Always returns a Dashboard object as we can always get the odometer value
        return Dashboard(
            self._endpoint_data["telemetry"]
            if "telemetry" in self._endpoint_data
            else None,
            self._endpoint_data["electric_status"]
            if "electric_status" in self._endpoint_data
            else None,
            self._endpoint_data["health_status"]
            if "health_status" in self._endpoint_data
            else None,
            self._metric,
        )

    @property
    def location(self) -> Optional[Location]:
        """Return the vehicles latest reported Location.

        Returns
        -------
          The latest location or None. If None vehicle car does not support
          providing location information.
          _Note_ an empty location object can be returned when the Vehicle
          supports location but none is currently available.
        """
        return (
            Location(self._endpoint_data["location"])
            if "location" in self._endpoint_data
            else None
        )

    @property  # TODO: Cant have a property with parameters! Split into two methods? # pylint: disable=W0511
    def notifications(self) -> Optional[List[Notification]]:  # noqa: PLR0206, ARG002
        """Returns a list of notifications for the vehicle.

        Args:
        ----
            include_read (bool, optional): Indicates whether to include read notifications. \n
            Defaults to False.

        Returns:
        -------
            Optional[List[Notification]]: A list of notifications for the vehicle,
            or None if not supported.

        """
        if "notifications" in self._endpoint_data:
            ret = []
            for p in self._endpoint_data["notifications"].payload:
                for n in p.notifications:
                    ret.append(Notification(n))

            return ret

        return None

    @property
    def lock_status(self) -> Optional[LockStatus]:
        """Returns the latest lock status of Doors & Windows.

        Returns
        -------
            Optional[LockStatus]: The latest lock status of Doors & Windows,
            or None if not supported.
        """
        return LockStatus(
            self._endpoint_data["status"] if "status" in self._endpoint_data else None
        )

    async def get_summary(
        self,
        from_date: date,
        to_date: date,
        summary_type: SummaryType = SummaryType.MONTHLY,
    ) -> Optional[List[Summary]]:
        """Return a Daily, Monthly or Yearly summary between the provided dates.

        Args:
        ----
            from_date (date, required): The inclusive from date to report summaries.
            to_date (date, required): The inclusive to date to report summaries.
            summary_type (???, optional): Daily, Monthly or Yearly summary. Monthly by default.

        Returns:
        -------
            Optional[List[Summary]]: A list of summaries or None if not supported.
        """
        if to_date > date.today():  # Future dates not allowed
            to_date = date.today()

        # Summary information is always returned in the first response.
        # No need to check all the following pages
        resp = await self._api.get_trips_endpoint(
            self.vin, from_date, to_date, summary=True, limit=1, offset=0
        )
        if resp.payload is None:
            return None

        # Convert to response
        ret: List[Summary] = []
        if summary_type == SummaryType.DAILY:
            for summary in resp.payload.summary:
                for histogram in summary.histograms:
                    summary_date = date(
                        day=histogram.day, month=histogram.month, year=histogram.year
                    )
                    ret.append(
                        Summary(
                            histogram.summary,
                            self._metric,
                            summary_date,
                            summary_date,
                            summary.hdc,
                        )
                    )
        elif summary_type == SummaryType.WEEKLY:
            raise NotImplementedError
        elif summary_type == SummaryType.MONTHLY:
            for summary in resp.payload.summary:
                summary_from_date = date(day=1, month=summary.month, year=summary.year)
                summary_to_date = date(
                    day=calendar.monthrange(summary.year, summary.month)[1],
                    month=summary.month,
                    year=summary.year,
                )

                ret.append(
                    Summary(
                        summary.summary,
                        self._metric,
                        summary_from_date
                        if summary_from_date > from_date
                        else from_date,
                        summary_to_date if summary_to_date < to_date else to_date,
                        summary.hdc,
                    )
                )
        elif summary_type == SummaryType.YEARLY:
            raise NotImplementedError

        return ret

    async def get_trips(
        self, from_date: date, to_date: date, full_route: bool = False
    ) -> Optional[List[Trip]]:
        """Return information on all trips made between the provided dates.

        Args:
        ----
            from_date (date, required): The inclusive from date
            to_date (date, required): The inclusive to date
            full_route (bool, optional): Provide the full route information for each trip

        Returns:
        -------
            Optional[List[Something]]: A list of all trips or None if not supported.
        """
        ret: List[Trip] = []
        offset = 0
        while True:
            resp = await self._api.get_trips_endpoint(
                self.vin,
                from_date,
                to_date,
                summary=False,
                limit=5,
                offset=offset,
                route=full_route,
            )
            if resp.payload is None:
                break

            # Convert to response
            for t in resp.payload.trips:
                ret.append(Trip(t, self._metric))

            offset = resp.payload.metadata.pagination.next_offset
            if offset is None:
                break

        return ret

    #
    # More get functionality depending on what we find
    #

    async def set_alias(self, value) -> bool:
        """Set the alias for the vehicle.

        Args:
        ----
            value: The alias value to set for the vehicle.

        Returns:
        -------
            bool
        """
        return value

    #
    # More set functionality depending on what we find
    #

    def _dump_all(self) -> Dict[str, Any]:
        """Dump data from all endpoints for debugging and further work."""
        dump: [str, Any] = {
            "vehicle_info": json.loads(self._vehicle_info.model_dump_json())
        }
        for name, data in self._endpoint_data.items():
            dump[name] = json.loads(data.model_dump_json())

        return censor_all(copy.deepcopy(dump))
