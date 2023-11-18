"""Vehicle model."""
import asyncio
import logging
from datetime import timedelta, datetime
from typing import Any
from functools import partial

from mytoyota.api import Api
from mytoyota.models.dashboard import Dashboard
from mytoyota.models.hvac import Hvac
from mytoyota.models.location import ParkingLocation

_LOGGER: logging.Logger = logging.getLogger(__package__)

class Vehicle:
    """Vehicle data representation."""

    def __init__(
            self,
            api: Api,
            vehicle_info: dict[str, Any],
            refresh_delay: timedelta = timedelta(minutes=1)
    ) -> None:
        assert ("vin" in vehicle_info)
        assert ("extendedCapabilities" in vehicle_info)

        self._vehicle_info = vehicle_info
        self._api = api
        self._endpoint_data: [str, Any] = {}

        # Endpoint Name, Function to check if car supports the endpoint, endpoint to call to update
        self._all_endpoints = [
                                ["location",
                                    partial(self._supports, "lastParkedCapable", "lastParked"),
                                    partial(self._api.get_location_endpoint, vin=vehicle_info["vin"])],
                                ["status",
                                    partial(self._supports, None, None),
                                    partial(self._api.get_vehicle_status_endpoint, vin=vehicle_info["vin"])],  # TODO Unsure of the required capability
                                ["electric_status",
                                    partial(self._supports, "econnectVehicleStatusCapable", None),
                                    partial(self._api.get_vehicle_electric_status_endpoint, vin=vehicle_info["vin"])],
                                ["telemetry",
                                    partial(self._supports, "telemetryCapable", None),
                                    partial(self._api.get_telemetry_endpoint, vin=vehicle_info["vin"])]
                              ]

    def _supports(self,
                  extendedCapability: str | None,
                  feature: str | None) -> bool:
        # If both set to None then nothing to check for
        if extendedCapability is None and feature is None:
            return True
        if extendedCapability is not None and self._vehicle_info["extendedCapabilities"][extendedCapability]:
            return True
        if feature is not None and self._vehicle_info["features"][feature] == 1:
            return True

        return False

    async def update(self):
        # TODO work out how to this is parallel
        for endpoint in self._all_endpoints:
            if endpoint[1]():
                self._endpoint_data[endpoint[0]] = await endpoint[2]()

    @property
    def vin(self) -> str | None:
        """Vehicle's vinnumber."""
        return self._vehicle_info.get("vin")

    @property
    def alias(self) -> str | None:
        """Vehicle's alias."""
        return self._vehicle_info.get("nickName", "Not set")

    async def set_alias(self, value) -> None:
        await self._api.set_vehicle_alias_endpoint(value, self._vehicle_info["subscriberGuid"], self.vin)

    @property
    def hybrid(self) -> bool:
        """If the vehicle is a hybrid."""
        # TODO need more details to check of electric cars return different capabilities
        return self._vehicle_info.get("evVehicle", False)

    @property
    def fueltype(self) -> str:
        """Fuel type of the vehicle."""
        fuel_type = self._vehicle_info.get("fuelType", "Unknown")
        if fuel_type != "Unknown":
            # Need to know further types. Only seen "I" or petrol cars.
            fuel_types = {"I": "Petrol"}
            if fuel_type in fuel_types:
                return fuel_types["fuelType"]
            else:
                logging.warning(f"Unknown fuel type: {fuel_type}")

        return "Unknown"

    @property
    def details(self) -> dict[str, Any] | None:
        """Formats vehicle info into a dict."""
        det: dict[str, Any] = {}
        for i in sorted(self._vehicle_info):
            if i in ("vin", "alias", "imei", "evVehicle"):
                continue
            det[i] = self._vehicle_info[i]
        return det if det else None

    @property
    def location(self) -> ParkingLocation | None:
        """Last parking location."""
        if "location" in self._endpoint_data:
            return ParkingLocation(self._endpoint_data["location"]["vehicleLocation"])

        return None

    @property
    def hvac(self) -> Hvac | None:
        """Vehicle hvac."""
        # This info is available need to find the endpoint.
        return None

    @property
    def dashboard(self) -> Dashboard | None:
        """Vehicle dashboard."""
        # Depending on car the required information is split across multiple endpoints
        # All cars seen have the status endpoint. This contains total milage.
        status = self._endpoint_data["telemetry"].copy()
        if "electric_status" in self._endpoint_data:
            status.update(self._endpoint_data["electric_status"])
            return Dashboard(status)

        return Dashboard(status)

    def _dump_all(self) -> dict[str, Any]:
        """ Helper function for collecting data for further work"""
        import pprint
        dump: [str, Any] = {"vehicle_info": self._vehicle_info}
        for name, data in self._endpoint_data.items():
            dump[name] = data

        return dump
