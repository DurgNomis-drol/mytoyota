"""Models for vehicle location."""
from datetime import datetime
from typing import Optional

from mytoyota.models.data import VehicleData


class ParkingLocation(VehicleData):
    """Parking Location data model."""

    @property
    def latitude(self) -> float:
        """Latitude."""
        return float(self._data.get("latitude", 0.0))

    @property
    def longitude(self) -> float:
        """Longitude."""
        return float(self._data.get("longitude", 0.0))

    @property
    def timestamp(self) -> Optional[datetime]:
        """Timestamp."""
        return self._data.get("locationAcquisitionDatetime")

    @property
    def state(self) -> str:
        return self._data.get("displayName")
