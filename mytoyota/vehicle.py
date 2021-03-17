"""Base classes"""
import logging
from typing import Optional

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Vehicle:  # pylint: disable=too-many-instance-attributes
    """Class to hold car information for each car"""

    def __init__(
        self,
        vehicle_info: Optional[dict],
        odometer: Optional[list],
        parking: Optional[dict],
        status: Optional[dict],
    ) -> None:
        self.odometer = None
        self.parking = None
        self.battery = None
        self.hvac = None
        self.error = None
        self.alias = vehicle_info["alias"] if "alias" in vehicle_info else None
        self.vin = vehicle_info["vin"] if "vin" in vehicle_info else None

        # If no vehicle information is provided, abort.
        if not vehicle_info:
            _LOGGER.error("No vehicle information provided")
            return

        # Format vehicle information.
        self.details = self.format_details(vehicle_info)

        # Extract odometer information.
        if not odometer:
            self.error = "Please setup Connected Services for your car"
        else:
            self.odometer = self.format_odometer(odometer)

        # Extract parking information.
        if not parking:
            self.error = "Please setup Connected Services for your car"
        else:
            self.parking = parking

        # Extracts information from status.
        self.extract_status(status)

    def __str__(self) -> str:
        return str(self.dict())

    def dict(self) -> dict:
        """Return car information in dict"""
        return {
            "alias": self.alias,
            "vin": self.vin,
            "details": self.details,
            "status": {
                "battery": self.battery,
                "hvac": self.hvac,
                "odometer": self.odometer,
                "parking": self.parking,
            },
            "error": self.error,
        }

    def extract_status(self, status) -> None:
        """Extract information like battery and hvac from status."""
        if "VehicleInfo" in status:
            if "RemoteHvacInfo" in status["VehicleInfo"]:
                self.hvac = status["VehicleInfo"]["RemoteHvacInfo"]

            if "ChargeInfo" in status["VehicleInfo"]:
                self.battery = status["VehicleInfo"]["ChargeInfo"]
        else:
            self.error = "Please setup Connected Services for your car"

    @staticmethod
    def format_odometer(raw):
        """Formats odometer information from a list to a dict."""
        instruments = {}
        for instrument in sorted(raw):
            instruments[instrument["type"]] = instrument["value"]
            if "unit" in instrument:
                instruments[instrument["type"] + "_unit"] = instrument["unit"]

        return instruments

    @staticmethod
    def format_details(raw):
        """Formats vehicle info into a dict."""
        details = {}
        for item in sorted(raw):
            if item in ("vin", "alias"):
                continue
            details[item] = raw[item]
        return details
