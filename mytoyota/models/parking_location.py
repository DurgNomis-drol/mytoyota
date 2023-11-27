"""Models for vehicle location."""
from datetime import datetime
from typing import Optional

from mytoyota.models.data import VehicleData


class ParkingLocation(VehicleData):
    """Parking Location data model."""

    @property
    def latitude(self) -> float:
        """Latitude."""
        return self._data.vehicleLocation.latitude

    @property
    def longitude(self) -> float:
        """Longitude."""
        return self._data.vehicleLocation.longitude

    @property
    def timestamp(self) -> Optional[datetime]:
        """Timestamp."""
        return self._data.vehicleLocation.locationAcquisitionDatetime

    @property
    def state(self) -> str:
        return self._data.vehicleLocation.displayName
