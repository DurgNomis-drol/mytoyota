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
from mytoyota.models.nofication import Notification
from mytoyota.models.parking_location import ParkingLocation
from mytoyota.utils.logs import censor_all

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Vehicle:
    """Vehicle data representation."""

    def __init__(
        self,
        api: Api,
        vehicle_info: VehicleGuidModel,
    ) -> None:
        self._vehicle_info = vehicle_info
        self._api = api
        self._endpoint_data: Dict[str, Any] = {}

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

    async def update(self):
        async def parallel_wrapper(name: str, function: partial) -> Tuple[str, Dict[str, Any]]:
            r = await function()
            return name, r

        responses = asyncio.gather(*[parallel_wrapper(name, function) for name, function in self._endpoint_collect])
        for name, data in await responses:
            self._endpoint_data[name] = data

    @property
    def vin(self) -> Optional[str]:
        """Vehicle's vinnumber."""
        return self._vehicle_info.vin

    @property
    def alias(self) -> Optional[str]:
        """Vehicle's alias."""
        return self._vehicle_info.nickname

    async def set_alias(self, value) -> None:
        await self._api.set_vehicle_alias_endpoint(value, self._vehicle_info.subscriber_guid, self.vin)

    @property
    def hybrid(self) -> bool:
        """If the vehicle is a hybrid."""
        # TODO need more details to check of electric cars return different capabilities
        return self._vehicle_info.ev_vehicle

    # @property
    # def fueltype(self) -> str:
    #    """Fuel type of the vehicle."""
    #    fuel_type = self._vehicle_info.get("fuelType", "Unknown")
    #    if fuel_type != "Unknown":
    #        # Need to know further types. Only seen "I" or petrol cars.
    #        fuel_types = {"I": "Petrol"}
    #        if fuel_type in fuel_types:
    #            return fuel_types["fuelType"]
    #        else:
    #            logging.warning(f"Unknown fuel type: {fuel_type}")
    #    return "Unknown"

    @property
    def details(self) -> Optional[Dict[str, Any]]:
        """Formats vehicle info into a dict."""
        det: Dict[str, Any] = {}
        for i in sorted(self._vehicle_info):
            if i in ("vin", "alias", "imei", "evVehicle"):
                continue
            det[i] = self._vehicle_info[i]
        return det if det else None

    @property
    def location(self) -> Optional[ParkingLocation]:
        """Last parking location."""
        if "location" in self._endpoint_data:
            return ParkingLocation(self._endpoint_data["location"])

        return None

    def notifications(self, include_read: bool = False) -> Optional[List[Notification]]:
        if "notifications" in self._endpoint_data:
            ret = []
            for notification in self._endpoint_data["notifications"]:
                if include_read or (notification["isRead"] is False):
                    ret.append(Notification(notification))

            return ret

        # TODO return an empty list or None? None because we dont support it?
        # TODO maybe add an API call to check what is supported
        # TODO throw a not supported exception? DataNotSupportedOnVehicle
        return None

    @property
    def hvac(self) -> Optional[Hvac]:
        """Vehicle hvac."""
        # This info is available need to find the endpoint.
        return None

    @property
    def dashboard(self) -> Optional[Dashboard]:
        """Vehicle dashboard."""
        # Depending on car the required information is split across multiple endpoints
        # All cars seen have the status endpoint. This contains total milage.
        status = self._endpoint_data["telemetry"].copy()
        if "electric_status" in self._endpoint_data:
            status.update(self._endpoint_data["electric_status"])
            return Dashboard(status)

        return Dashboard(status)

    def _dump_all(self) -> Dict[str, Any]:
        """Helper function for collecting data for further work"""
        dump: [str, Any] = {"vehicle_info": json.loads(self._vehicle_info.model_dump_json())}
        for name, data in self._endpoint_data.items():
            dump[name] = json.loads(data.model_dump_json())

        return censor_all(copy.deepcopy(dump))
