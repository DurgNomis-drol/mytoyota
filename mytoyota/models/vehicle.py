"""Vehicle model."""
import asyncio
import copy
from functools import partial
import logging
from typing import Any, Optional

from mytoyota.api import Api
from mytoyota.models.dashboard import Dashboard
from mytoyota.models.hvac import Hvac
from mytoyota.models.location import ParkingLocation
from mytoyota.models.nofication import Notification
from mytoyota.utils.logs import censor_all

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Vehicle:
    """Vehicle data representation."""

    def __init__(
        self,
        api: Api,
        vehicle_info: dict[str, Any],
    ) -> None:
        assert "vin" in vehicle_info
        assert "extendedCapabilities" in vehicle_info

        self._vehicle_info = vehicle_info
        self._api = api
        self._endpoint_data: [str, Any] = {}

        # Endpoint Name, Function to check if car supports the endpoint, endpoint to call to update
        all_endpoints = [
            [
                "location",
                partial(self._supported, "lastParkedCapable", "lastParked"),
                partial(self._api.get_location_endpoint, vin=vehicle_info["vin"]),
            ],
            [
                "health_status",
                partial(
                    self._supported, None, None
                ),  # TODO Unsure of the required capability
                partial(
                    self._api.get_vehicle_health_status_endpoint,
                    vin=vehicle_info["vin"],
                ),
            ],
            [
                "electric_status",
                partial(self._supported, "econnectVehicleStatusCapable", None),
                partial(
                    self._api.get_vehicle_electric_status_endpoint,
                    vin=vehicle_info["vin"],
                ),
            ],
            [
                "telemetry",
                partial(self._supported, "telemetryCapable", None),
                partial(self._api.get_telemetry_endpoint, vin=vehicle_info["vin"]),
            ],
            [
                "notifications",
                partial(
                    self._supported, None, None
                ),  # TODO Unsure of the required capability
                partial(self._api.get_notification_endpoint, vin=vehicle_info["vin"]),
            ],
            [
                "status",
                partial(self._supported, "vehicleStatus", None),
                partial(self._api.get_vehicle_status_endpoint, vin=vehicle_info["vin"]),
            ],
        ]
        self._endpoint_collect: list[tuple[str, partial]] = []
        for ep in all_endpoints:
            if ep[1]():
                self._endpoint_collect.append((ep[0], ep[2]))

    def _supported(
        self, extendedCapability: Optional[str], feature: Optional[str]
    ) -> bool:
        # If both set to None then nothing to check for
        if extendedCapability is None and feature is None:
            return True
        if (
            extendedCapability is not None
            and self._vehicle_info["extendedCapabilities"][extendedCapability]
        ):
            return True
        if feature is not None and self._vehicle_info["features"][feature] == 1:
            return True

        return False

    async def update(self):
        async def parallel_wrapper(
            name: str, fn: partial
        ) -> tuple[str, dict[str, Any]]:
            r = await fn()
            return name, r

        responses = asyncio.gather(
            *[parallel_wrapper(ep[0], ep[1]) for ep in self._endpoint_collect]
        )
        for name, data in await responses:
            self._endpoint_data[name] = data

    @property
    def vin(self) -> Optional[str]:
        """Vehicle's vinnumber."""
        return self._vehicle_info.get("vin")

    @property
    def alias(self) -> Optional[str]:
        """Vehicle's alias."""
        return self._vehicle_info.get("nickName", "Not set")

    async def set_alias(self, value) -> None:
        await self._api.set_vehicle_alias_endpoint(
            value, self._vehicle_info["subscriberGuid"], self.vin
        )

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
    def details(self) -> Optional[dict[str, Any]]:
        """Formats vehicle info into a dict."""
        det: dict[str, Any] = {}
        for i in sorted(self._vehicle_info):
            if i in ("vin", "alias", "imei", "evVehicle"):
                continue
            det[i] = self._vehicle_info[i]
        return det if det else None

    @property
    def location(self) -> Optional[ParkingLocation]:
        """Last parking location."""
        if "location" in self._endpoint_data:
            return ParkingLocation(self._endpoint_data["location"]["vehicleLocation"])

        return None

    def notifications(self, include_read: bool = False) -> Optional[list[Notification]]:
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

    def _dump_all(self) -> dict[str, Any]:
        """Helper function for collecting data for further work"""
        dump: [str, Any] = {"vehicle_info": self._vehicle_info}
        for name, data in self._endpoint_data.items():
            if name == "notifications":
                dump[name] = data[:5]
            else:
                dump[name] = data

        return censor_all(copy.deepcopy(dump))
