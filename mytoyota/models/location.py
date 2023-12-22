"""Models for vehicle location."""
from datetime import datetime
from typing import Optional

from mytoyota.models.endpoints.location import LocationResponseModel


class Location:
    """Latest Location of car."""

    def __init__(self, location: Optional[LocationResponseModel] = None):
        """Init the location model."""
        self._location = None
        if location and location.payload:
            self._location = location.payload.vehicle_location

    def __repr__(self):
        """Representation of the location model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def latitude(self) -> Optional[float]:
        """Latitude.

        Returns
        -------
            Latest latitude or None. _Not always available_.
        """
        return self._location.latitude if self._location else None

    @property
    def longitude(self) -> Optional[float]:
        """Longitude.

        Returns
        -------
            Latest longitude or None. _Not always available_.
        """
        return self._location.longitude if self._location else None

    @property
    def timestamp(self) -> Optional[datetime]:
        """Timestamp.

        Returns
        -------
           Position aquired timestamp or None. _Not always available_.
        """
        return self._location.location_acquisition_datetime if self._location else None

    @property
    def state(self) -> str:
        """State.

        Returns
        -------
          The state of the position or None. _Not always available_.
        """
        return self._location.display_name if self._location else None
