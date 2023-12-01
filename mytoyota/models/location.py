"""Models for vehicle location."""
from datetime import datetime
from typing import Optional

from mytoyota.models.endpoints.location import LocationResponseModel


class Location:
    """
    Latest Location of car
    """

    def __init__(self, location: Optional[LocationResponseModel] = None):
        self._location = None
        if location and location.payload:
            self._location = location.payload.vehicle_location

    def __repr__(self):
        return " ".join(
            [f"{k}={str(getattr(self, k))}" for k, v in type(self).__dict__.items() if isinstance(v, property)]
        )

    @property
    def latitude(self) -> Optional[float]:
        """
        Latitude.

        returns
            Latest latitude or None. _Not always available_.
        """
        return self._location.latitude if self._location else None

    @property
    def longitude(self) -> Optional[float]:
        """
        Longitude.

        returns
            Latest longitude or None. _Not always available_.
        """
        return self._location.longitude if self._location else None

    @property
    def timestamp(self) -> Optional[datetime]:
        """
        Timestamp.

        returns
           Position aquired timestamp or None. _Not always available_.
        """
        return self._location.location_acquisition_datetime if self._location else None

    @property
    def state(self) -> str:
        """
        State.

        returns
          The state of the position or None. _Not always available_.
        """
        return self._location.display_name if self._location else None
