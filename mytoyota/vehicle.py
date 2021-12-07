"""Vehicle representation"""
import logging
from typing import Optional

from mytoyota.hvac import Hvac
from mytoyota.location import ParkingLocation
from mytoyota.status import Energy, Odometer, Sensors
from mytoyota.utils.formatters import format_odometer
from mytoyota.utils.logs import censor_vin

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


class Vehicle:
    """Vehicle representation"""

    is_connected: bool = False
    details: Optional[dict] = None
    odometer: Optional[Odometer] = None
    energy: Optional[Energy] = None
    hvac: Optional[Hvac] = None
    parking: Optional[ParkingLocation] = None
    sensors: Optional[Sensors] = None
    statistics: VehicleStatistics = VehicleStatistics()

    def __init__(  # pylint: disable=too-many-branches
        self,
        vehicle_info: dict,
        connected_services: Optional[dict] = None,
        odometer: Optional[list] = None,
        status: Optional[dict] = None,
        remote_control: Optional[dict] = None,
    ) -> None:

        # If no vehicle information is provided, abort.
        if not vehicle_info:
            _LOGGER.error("No vehicle information provided!")
            return

        # Vehicle information
        self.id = vehicle_info.get("id", None)  # pylint: disable=invalid-name
        self.vin = vehicle_info.get("vin", None)
        self.alias = vehicle_info.get("alias", None)

        # Format vehicle details.
        self.details = self._format_details(vehicle_info)

        self.is_connected = (
            self._has_connected_services_enabled(connected_services)
            if connected_services
            else False
        )

        if self.is_connected and self.vin:

            remote_control_info = (
                remote_control.get("VehicleInfo") if remote_control is not None else {}
            )

            # Extract mileage and if the car reports in km or mi
            self.odometer = (
                Odometer(format_odometer(odometer)) if odometer else Odometer({})
            )

            # Extract fuel level/Energy capacity information from status.
            if status and "energy" in status:
                _LOGGER.debug("Using energy data: %s", str(status.get("energy")))
                self.energy = Energy(status.get("energy"), self.odometer.unit)
            # Use legacy odometer to get fuel level. Older cars still uses this.
            elif odometer:
                _LOGGER.debug("Using legacy odometer data: %s", str(odometer))
                self.energy = Energy(
                    format_odometer(odometer), self.odometer.unit, True
                )
                fueltype = self.details.get("fuel", "Unknown")
                # PATCH: Toyota Aygo reports wrong type.
                if fueltype == "1.0P":
                    fueltype = "Petrol"
                self.energy.type = fueltype
                # Add charge information if car supports it.
                if remote_control_info and "ChargeInfo" in remote_control_info:
                    self.energy.set_battery_attributes(
                        remote_control_info.get("ChargeInfo", {})
                    )

            if status:
                # Extract parking information from status.
                self.parking = ParkingLocation(status.get("event", {}))

                # Extracts window, door, lock and other information from status.
                self.sensors = Sensors(status.get("protectionState", {}))

            # Extract HVAC information from endpoint
            if remote_control_info and "RemoteHvacInfo" in remote_control_info:
                self.hvac = Hvac(remote_control_info.get("RemoteHvacInfo", {}), True)
            elif status and "climate" in status:
                self.hvac = Hvac(status.get("climate"))
            else:
                self.hvac = None

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
                "energy": self.energy.as_dict(),
                "hvac": self.hvac.as_dict() if self.hvac is not None else {},
                "odometer": self.odometer.as_dict(),
                "parking": self.parking.as_dict(),
                "vehicle": self.sensors.as_dict(),
            },
            "servicesEnabled": {
                "connectedServices": self.is_connected,
            },
            "statistics": self.statistics.as_dict(),
        }

    def _has_connected_services_enabled(self, json_dict: dict) -> bool:
        """Checks if the user has enabled connected services."""
        # Check if vin is not None. Toyota's servers is a bit flacky and can
        # return garbage from connected_services endpoint, this is just to
        # make sure that we don't throw a error message.
        if self.vin:
            if (
                "connectedService" in json_dict
                and "status" in json_dict["connectedService"]
            ):
                if json_dict["connectedService"]["status"] == "ACTIVE":
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

    @staticmethod
    def _format_details(raw: dict) -> dict:
        """Formats vehicle info into a dict."""
        details: dict = {}
        for item in sorted(raw):
            if item in ("vin", "alias", "id"):
                continue
            details[item] = raw[item]
        return details
