"""Vehicle model."""
from __future__ import annotations

import logging
from typing import Any

from mytoyota.models.dashboard import Dashboard
from mytoyota.models.hvac import Hvac
from mytoyota.models.location import ParkingLocation
from mytoyota.models.sensors import Sensors
from mytoyota.utils.formatters import format_odometer
from mytoyota.utils.logs import censor_vin

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Vehicle:
    """Vehicle data representation."""

    def __init__(
        self,
        vehicle_info: dict[str, Any],
        connected_services: dict[str, Any],
        odometer: list[Any] | None = None,
        status: dict[str, Any] | None = None,
        status_legacy: dict[str, Any] | None = None,
    ) -> None:

        self._connected_services = connected_services
        self._vehicle_info = vehicle_info

        self.odometer = format_odometer(odometer) if odometer else {}
        self._status = status if status else {}
        self._status_legacy = status_legacy if status_legacy else {}

    @property
    def vehicle_id(self) -> int | None:
        """Vehicle's id."""
        return self._vehicle_info.get("id")

    @property
    def vin(self) -> str | None:
        """Vehicle's vinnumber."""
        return self._vehicle_info.get("vin")

    @property
    def alias(self) -> str | None:
        """Vehicle's alias."""
        return self._vehicle_info.get("alias", "My vehicle")

    @property
    def hybrid(self) -> bool:
        """If the vehicle is a hybrid."""
        return self._vehicle_info.get("hybrid", False)

    @property
    def fueltype(self) -> str:
        """Fuel type of the vehicle."""
        if self._status:
            if "energy" in self._status and self._status["energy"]:
                return self._status["energy"][0].get("type", "Unknown").capitalize()

        fueltype = self._vehicle_info.get("fuel", "Unknown")
        return "Petrol" if fueltype == "1.0P" else fueltype

    @property
    def details(self) -> dict[str, Any] | None:
        """Formats vehicle info into a dict."""
        det: dict[str, Any] = {}
        for i in sorted(self._vehicle_info):
            if i in ("vin", "alias", "id", "hybrid"):
                continue
            det[i] = self._vehicle_info[i]
        return det if det else None

    @property
    def is_connected_services_enabled(self) -> bool:
        """Checks if the user has enabled connected services."""
        # Check if vin is not None. Toyota's servers is a bit flacky and can
        # return garbage from connected_services endpoint, this is just to
        # make sure that we don't throw a error message.
        if self.vin and self._connected_services:
            if (
                "connectedService" in self._connected_services
                and "status" in self._connected_services["connectedService"]
            ):
                if self._connected_services["connectedService"]["status"] == "ACTIVE":
                    return True

                _LOGGER.error(
                    "Please setup Connected Services if you want live data from the car. (%s)",
                    censor_vin(self.vin),
                )
                return False
            _LOGGER.error(
                "Your vehicle does not support Connected services (%s). You can find out if your "
                "vehicle is compatible by checking the manual that comes with your car.",
                censor_vin(self.vin),
            )
        return False

    @property
    def parkinglocation(self) -> ParkingLocation | None:
        """Last parking location."""
        if self.is_connected_services_enabled and "event" in self._status:
            return ParkingLocation(self._status.get("event"))
        return None

    @property
    def sensors(self) -> Sensors | None:
        """Vehicle sensors."""
        if self.is_connected_services_enabled and self._status:
            if "protectionState" in self._status:
                return Sensors(self._status.get("protectionState"))
        return None

    @property
    def hvac(self) -> Hvac | None:
        """Vehicle hvac."""
        if self.is_connected_services_enabled:
            if self._status and "climate" in self._status:
                return Hvac(self._status.get("climate"))
            if self._status_legacy:
                rci = self._status_legacy.get("VehicleInfo", {})
                if "RemoteHvacInfo" in rci:
                    return Hvac(rci.get("RemoteHvacInfo"), True)
        return None

    @property
    def dashboard(self) -> Dashboard | None:
        """Vehicle dashboard."""
        if self.is_connected_services_enabled and self.odometer:
            return Dashboard(self)
        return None
