"""Models for vehicle location."""
from __future__ import annotations

from mytoyota.models.data import VehicleData


class ParkingLocation(VehicleData):
    """Parking Location data model."""

    @property
    def latitude(self) -> float:
        """Latitude."""
        return float(self._data.get("lat", 0.0))

    @property
    def longitude(self) -> float:
        """Longitude."""
        return float(self._data.get("lon", 0.0))

    @property
    def timestamp(self) -> int | None:
        """Timestamp."""
        return self._data.get("timestamp")
