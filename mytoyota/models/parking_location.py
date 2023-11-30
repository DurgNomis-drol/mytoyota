"""Models for vehicle location."""
from datetime import datetime
from typing import Optional

from mytoyota.models.data import VehicleData


class ParkingLocation(VehicleData):
    """Parking Location data model."""

    @property
    def latitude(self) -> float:
        """Latitude."""
        return self._data.payload.vehicle_location.latitude

    @property
    def longitude(self) -> float:
        """Longitude."""
        return self._data.payload.vehicle_location.longitude

    @property
    def timestamp(self) -> Optional[datetime]:
        """Timestamp."""
        return self._data.payload.vehicle_location.location_acquisition_datetime

    @property
    def state(self) -> str:
        """State."""
        return self._data.payload.vehicle_location.display_name
