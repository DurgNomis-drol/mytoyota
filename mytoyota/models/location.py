"""Models for vehicle location."""
from __future__ import annotations


from sqlite3 import Timestamp
from mytoyota.models.data import VehicleData


class ParkingLocation(VehicleData):
    """Parking Location data model."""

    @property
    def latitude(self) -> float:
        return float(self._data.get("lat", 0.0))
    
    @property
    def longitude(self) -> float:
        return float(self._data.get("lon", 0.0))
    
    @property
    def timestamp(self) -> int | None:
        return self._data.get("timestamp")
