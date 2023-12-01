"""Vehicle model."""
import asyncio
import copy
import json
import logging
from datetime import date, timedelta
from functools import partial
from typing import Any, Dict, List, Optional, Tuple

from mytoyota.api import Api
from mytoyota.models.dashboard import Dashboard
from mytoyota.models.endpoints.vehicle_guid import VehicleGuidModel
from mytoyota.models.hvac import Hvac
from mytoyota.models.location import Location
from mytoyota.models.nofication import Notification
from mytoyota.utils.logs import censor_all

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Vehicle:
    """Vehicle data representation."""

    def __init__(self, api: Api, vehicle_info: VehicleGuidModel, metric: bool = True) -> None:
        """Initialise the Vehicle data representation."""
        self._vehicle_info = vehicle_info
        self._api = api
        self._endpoint_data: Dict[str, Any] = {}
        self._metric = metric

        # Endpoint Name, Function to check if car supports the endpoint, endpoint to call to update
        api_endpoints = [
            {
                "name": "location",
                "capable": vehicle_info.extended_capabilities.last_parked_capable or vehicle_info.features.last_parked,
                "function": partial(self._api.get_location_endpoint, vin=vehicle_info.vin),
            },
            {
                "name": "health_status",
                "capable": True,  # TODO Unsure of the required capability
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
                "function": partial(self._api.get_telemetry_endpoint, vin=vehicle_info.vin),
            },
            {
                "name": "notifications",
                "capable": True,  # TODO Unsure of the required capability
                "function": partial(self._api.get_notification_endpoint, vin=vehicle_info.vin),
            },
            {
                "name": "status",
                "capable": vehicle_info.extended_capabilities.vehicle_status,
                "function": partial(self._api.get_remote_status_endpoint, vin=vehicle_info.vin),
            },
            {
                "name": "trips",
                "capable": True,  # TODO Unsure of the required capability
                "function": partial(
                    self._api.get_trips_endpoint,
                    vin=vehicle_info.vin,
                    from_date=date.today() - timedelta(days=1),
                    to_date=date.today(),
                ),
            },
        ]
        self._endpoint_collect = [
            (endpoint["name"], endpoint["function"]) for endpoint in api_endpoints if endpoint["capable"]
        ]

    async def update(self) -> None:
        """Update the data for the vehicle.

        This method asynchronously updates the data for the vehicle by calling the endpoint functions in parallel.

        Returns
        -------
            None

        """

        async def parallel_wrapper(name: str, function: partial) -> Tuple[str, Dict[str, Any]]:
            r = await function()
            return name, r

        responses = asyncio.gather(*[parallel_wrapper(name, function) for name, function in self._endpoint_collect])
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
        # TODO enum
        # TODO currently guessing until we see a mild hybrid and full EV
        # TODO should probably use electricalPlatformCode but values currently unknown
        # TODO list of fuel types. ?: G=Petrol Only, I=Hybrid
        return "phev" if self._vehicle_info.ev_vehicle and self._vehicle_info.fuel_type else "ev"

    @property
    def dashboard(self) -> Optional[Dashboard]:
        """Returns the Vehicle dashboard.

        The dashboard consists of items of information you would expect to find on the dashboard. i.e. Fuel Levels

        Returns
        -------
            A dashboard
        """
        # Always returns a Dashboard object as we can always get the odometer value
        return Dashboard(
            self._endpoint_data["telemetry"] if "telemetry" in self._endpoint_data else None,
            self._endpoint_data["electric_status"] if "electric_status" in self._endpoint_data else None,
            self._endpoint_data["health_status"] if "health_status" in self._endpoint_data else None,
            self._metric,
        )

    @property
    def location(self) -> Optional[Location]:
        """Return the vehicles latest reported Location.

        Returns
        -------
          The latest location or None. If None vehicle car does not support providing location information.
          _Note_ an empty location object can be returned when the Vehicle supports location but none is currently
          available.
        """
        return Location(self._endpoint_data["location"]) if "location" in self._endpoint_data else None

    @property  # TODO: Cant have a property with parameters! Split into two methods?
    def notifications(self, include_read: bool = False) -> Optional[List[Notification]]:  # noqa: PLR0206, ARG002
        """Returns a list of notifications for the vehicle.

        Args:
        ----
            include_read (bool, optional): Indicates whether to include read notifications. Defaults to False.

        Returns:
        -------
            Optional[List[Notification]]: A list of notifications for the vehicle, or None if not supported.

        """
        return None

    @property
    def hvac(self) -> Optional[Hvac]:
        """Vehicle hvac."""
        # This info is available need to find the endpoint.
        return None

    @property
    def locks_status(self) -> Optional[Any]:
        """Returns the latest status of Doors & Windows.

        Args:
        ----
            include_read (bool, optional): Indicates whether to include read notifications. Defaults to False.

        Returns:
        -------
            Optional[List[Notification]]: A list of notifications for the vehicle, or None if not supported.
        """
        return None

    async def get_summary(self, from_date: date, to_date: date, summary_type) -> Optional[List[Any]]:  # noqa: ARG002
        """Return a Daily, Monthly or Yearly summary between the provided dates.

        Args:
        ----
            from_date (date, required): The inclusive from date to report summaries.
            to_date (date, required): The inclusive to date to report summaries.
            summary_type (???, optional): Daily, Monthly or Yearly summary. Monthly by default.

        Returns:
        -------
            Optional[List[Something]]: A list of summaries or None if not supported.
        """
        return None

    async def get_trips(self, from_date: date, to_date: date, full_route: bool = False) -> Optional[List[Any]]:  # noqa: ARG002
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
        return None

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
            None
        """
        pass

    #
    # More set functionality depending on what we find
    #

    def _dump_all(self) -> Dict[str, Any]:
        """Dump data from all endpoints for debugging and further work."""
        dump: [str, Any] = {"vehicle_info": json.loads(self._vehicle_info.model_dump_json())}
        for name, data in self._endpoint_data.items():
            dump[name] = json.loads(data.model_dump_json())

        return censor_all(copy.deepcopy(dump))
