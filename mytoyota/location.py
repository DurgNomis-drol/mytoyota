"""Location representation for mytoyota"""
import logging

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ParkingLocation:
    """ParkingLocation representation"""

    latitude: float = 0.0
    longitude: float = 0.0
    timestamp: int = 0

    def __init__(self, parking: dict) -> None:
        self.latitude = float(parking.get("lat", 0.0))
        self.longitude = float(parking.get("lon", 0.0))
        self.timestamp = int(parking.get("timestamp", 0))

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return parking location as dict."""
        return vars(self)
