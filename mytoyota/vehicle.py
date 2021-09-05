"""Vehicle class"""
import logging
from typing import Optional

from mytoyota.const import DOORS, HOOD, KEY, LIGHTS, WINDOWS
from mytoyota.models import Doors, Key, Lights, Windows

_LOGGER: logging.Logger = logging.getLogger(__package__)


class VehicleStatistics:
    """Vehicle statistics representation"""

    daily: list = None
    weekly: list = None
    monthly: list = None
    yearly: list = None

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return vehicle statistics as dict."""
        return vars(self)


class Odometer:
    """Odometer representation"""

    mileage: int = None
    unit: str = None
    fuel: int = None

    def __init__(self, odometer: Optional[list]) -> None:

        _LOGGER.debug("Raw odometer data: %s", str(odometer))

        if odometer is not None:

            odometer_dict = self._format_odometer(odometer)

            _LOGGER.debug("Formatted odometer data: %s", str(odometer_dict))

            if "mileage" in odometer_dict:
                self.mileage = odometer_dict["mileage"]
            if "mileage_unit" in odometer_dict:
                self.unit = odometer_dict["mileage_unit"]
            if "Fuel" in odometer_dict:
                self.fuel = odometer_dict["Fuel"]

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return odometer as dict."""
        return vars(self)

    @staticmethod
    def _format_odometer(raw: list) -> dict:
        """Formats odometer information from a list to a dict."""
        instruments: dict = {}
        for instrument in raw:
            instruments[instrument["type"]] = instrument["value"]
            if "unit" in instrument:
                instruments[instrument["type"] + "_unit"] = instrument["unit"]

        return instruments


class ParkingLocation:
    """ParkingLocation representation"""

    latitude: float = None
    longitude: float = None
    timestamp: int = None

    def __init__(self, parking: Optional[dict]) -> None:
        _LOGGER.debug("Raw parking location data: %s", str(parking))

        if parking is not None:
            self.latitude = float(parking["lat"])
            self.longitude = float(parking["lon"])
            self.timestamp = int(parking["timestamp"])

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return parking location as dict."""
        return vars(self)


class Status:
    """Vehicle status representation"""

    lights: Optional[Lights] = None
    doors: Optional[Doors] = None
    windows: Optional[Windows] = None
    key: Optional[Key] = None

    overallstatus: str = None
    last_updated: str = None

    def __init__(self, status: Optional[dict]):

        _LOGGER.debug("Raw status data: %s", str(status))

        if status is not None:
            self.overallstatus = status["overallStatus"]

            self.lights = Lights(status[LIGHTS])
            self.doors = Doors(status[HOOD], status[DOORS])
            self.windows = Windows(status[WINDOWS])
            self.key = Key(status[KEY])

            self.last_updated = status["timestamp"]

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return {
            "overallstatus": self.overallstatus,
            "lights": self.lights.as_dict() if self.lights is not None else None,
            "doors": self.doors.as_dict() if self.doors is not None else None,
            "windows": self.windows.as_dict() if self.windows is not None else None,
            "key": self.key.as_dict() if self.key is not None else None,
            "last_updated": self.last_updated,
        }


class Vehicle:  # pylint: disable=too-many-instance-attributes
    """Vehicle representation"""

    id: int = 0
    vin: str = None
    alias: str = None
    is_connected: bool = False
    details: Optional[dict] = None
    odometer: Optional[Odometer] = None
    parking: Optional[ParkingLocation] = None
    statistics: VehicleStatistics = VehicleStatistics()
    status: Optional[Status] = None

    def __init__(  # pylint: disable=too-many-arguments
        self,
        vehicle_info: dict,
        connected_services: Optional[dict],
        odometer: Optional[list],
        status: Optional[dict],
    ) -> None:

        # If no vehicle information is provided, abort.
        if not vehicle_info:
            _LOGGER.error("No vehicle information provided!")
            return

        _LOGGER.debug("Raw connected services data: %s", str(connected_services))

        if connected_services is not None:
            self.is_connected = self._has_connected_services_enabled(connected_services)

        _LOGGER.debug("Raw vehicle info: %s", str(vehicle_info))

        # Vehicle information
        if "id" in vehicle_info:
            self.id = vehicle_info["id"]  # pylint: disable=invalid-name
        if "vin" in vehicle_info:
            self.vin = vehicle_info["vin"]
        if "alias" in vehicle_info:
            self.alias = vehicle_info["alias"]

        # Format vehicle information.
        self.details = self._format_details(vehicle_info)

        if self.is_connected:
            # Extract odometer information.
            self.odometer = Odometer(odometer) if odometer else Odometer(None)

            _LOGGER.debug("Raw status data: %s", str(status))

            # Extract parking information.
            self.parking = (
                ParkingLocation(status["event"])
                if "event" in status
                else ParkingLocation(None)
            )

            # Extracts information from status.
            self.status = (
                Status(status["protectionState"])
                if "protectionState" in status
                else Status(None)
            )

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return vehicle as dict."""
        return {
            "id": self.id,
            "alias": self.alias,
            "vin": self.vin,
            "details": self.details,
            "status": {
                "odometer": self.odometer.as_dict(),
                "parking": self.parking.as_dict(),
                "vehicle": self.status.as_dict(),
            },
            "servicesEnabled": {
                "connectedServices": self.is_connected,
            },
            "statistics": self.statistics.as_dict(),
        }

    def _has_connected_services_enabled(self, json_dict: dict) -> bool:
        """Checks if the user has enabled connected services."""

        if (
            "connectedService" in json_dict
            and "status" in json_dict["connectedService"]
        ):
            if json_dict["connectedService"]["status"] == "ACTIVE":
                return True

            _LOGGER.error(
                "Please setup Connected Services if you want live data from the car. (%s)",
                self.vin,
            )
            return False
        _LOGGER.error(
            "Your vehicle does not support Connected services (%s). You can find out if your "
            "vehicle is compatible by checking the manual that comes with your car.",
            self.vin,
        )
        return False

    @staticmethod
    def _format_details(raw: dict) -> dict:
        """Formats vehicle info into a dict."""
        details: dict = {}
        for item in sorted(raw):
            if item in ("vin", "alias", "id"):
                continue
            details[item] = raw[item]
        return details
