"""Model for Trip Summaries."""
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

from mytoyota.models.endpoints.trips import _TripModel
from mytoyota.utils.conversions import convert_distance


class Trip:
    """Base class of Daily, Weekly, Monthly, Yearly summary."""

    def __init__(
        self,
        trip: _TripModel,
        metric: bool,
    ):
        """Initialise Class.

        Args:
        ----
            trip (_TripModel, required): Contains all information regarding the trip
            metric (bool, required): Report in Metric or Imperial
        """
        self._trip = trip
        self._metric = "km" if metric else "mi"

    def __repr__(self):
        """Representation of MonthSummary."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def start_location(self) -> Tuple[float, float]:
        """Start location.

        Returns
        -------
            Tuple[float, float]: Start location (Lat, Lon)
        """
        return self._trip.summary.start_lat, self._trip.summary.start_lon

    @property
    def end_location(self) -> Tuple[float, float]:
        """End location.

        Returns
        -------
            Tuple[float, float]: End location (Lat, Lon)
        """
        return self._trip.summary.end_lat, self._trip.summary.end_lon

    @property
    def start_time(self) -> datetime:
        """Start time.

        Returns
        -------
            datetime: Start time of trip
        """
        return self._trip.summary.start_ts

    @property
    def end_time(self) -> datetime:
        """End time.

        Returns
        -------
            datetime: End time of trip
        """
        return self._trip.summary.end_ts

    @property
    def duration(self) -> timedelta:
        """The total time driving.

        Returns
        -------
            timedelta: The amount of time driving
        """
        return timedelta(seconds=self._trip.summary.duration)

    @property
    def distance(self) -> float:
        """The total distance covered.

        Returns
        -------
            float: Distance covered in the selected metric
        """
        return convert_distance(self._metric, "km", self._trip.summary.length / 1000.0)

    @property
    def ev_duration(self) -> Optional[timedelta]:
        """The total time driving using EV.

        Returns
        -------
            timedelta: The amount of time driving using EV or None if not supported
        """
        return timedelta(seconds=self._trip.hdc.ev_time) if self._trip.hdc else None

    @property
    def ev_distance(self) -> Optional[float]:
        """The total time distance driven using EV.

        Returns
        -------
            timedelta: The distance driven using EV in selected metric or None if not supported
        """
        return (
            convert_distance(self._metric, "km", self._trip.hdc.ev_distance / 1000.0)
            if self._trip.hdc
            else None
        )

    @property
    def fuel_consumed(self) -> float:
        """The amount of fuel consumed.

        Returns
        -------
            float: The fuel consumed in liters if metric or gallons
        """
        if self._trip.summary.fuel_consumption:
            return (
                round(self._trip.summary.fuel_consumption / 4546.0, 3)
                if self._metric
                else (self._trip.summary.fuel_consumption / 1000.0)
            )

        return 0.0

    @property
    def route(self) -> Optional[List[Tuple[float, float]]]:
        """The route taken.

        Returns
        -------
            Optional[List[Tuple[float, float]]]: List of Lat, Lon of the route taken.
                None if no route provided.
        """
        if self._trip.route:
            return [(rm.lat, rm.lon) for rm in self._trip.route]

        return None
