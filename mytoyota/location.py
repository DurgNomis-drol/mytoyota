"""Location representation for mytoyota"""
import logging

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ParkingLocation:
    """ParkingLocation representation"""

    latitude: float = None
    longitude: float = None
    timestamp: int = None

    def __init__(self, parking: dict) -> None:
        _LOGGER.debug("Raw parking location data: %s", str(parking))

        self.latitude = float(parking.get("lat", None))
        self.longitude = float(parking.get("lon", None))
        self.timestamp = int(parking.get("timestamp", None))

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return parking location as dict."""
        return vars(self)
