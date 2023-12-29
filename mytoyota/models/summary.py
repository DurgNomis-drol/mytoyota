"""Model for Trip Summaries."""
from datetime import date, timedelta
from enum import IntEnum
from typing import List, Optional

from mytoyota.models.endpoints.trips import _HDCModel, _SummaryBaseModel
from mytoyota.utils.conversions import convert_distance


class SummaryType(IntEnum):
    """Type of summary for use with get_summary."""

    DAILY = 1
    WEEKLY = 2
    MONTHLY = 3
    YEARLY = 4


class Summary:
    """Base class of Daily, Weekly, Monthly, Yearly summary."""

    def __init__(  # noqa: PLR0913
        self,
        summary: _SummaryBaseModel,
        metric: bool,
        from_date: date,
        to_date: date,
        hdc: Optional[_HDCModel] = None,
    ):
        """Initialise Class.

        Args:
        ----
            summary (_SummaryBaseModel, required): Contains all the summary information
            metric (bool, required): Report in Metric or Imperial
            from_date (date, required): Start date for this summary
            to_date (date, required): End date for this summary
            hdc: (_HDCModel, optional): Hybrid data if available
        """
        self._summary = summary
        self._hdc = hdc
        self._metric = "km" if metric else "mi"
        self._from_date = from_date
        self._to_date = to_date

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
    def average_speed(self) -> float:
        """Average speed.

        Returns:
        -------
            float: Average speed in selected metric
                Return information on all trips made between the provided dates.

        Args:
        ----
            from_date (date, required): The inclusive from date
            to_date (date, required): The inclusive to date
            full_route (bool, optional): Provide the full route information for each trip

        """
        return convert_distance(self._metric, "km", self._summary.average_speed)

    @property
    def countries(self) -> List[str]:
        """Countries visited.

        Returns
        -------
            List[str]: List of countries visited in 'ISO 3166-1 alpha-2' or
                two-letter country codes format.
        """
        return self._summary.countries

    @property
    def duration(self) -> timedelta:
        """The total time driving.

        Returns
        -------
            timedelta: The amount of time driving
        """
        return timedelta(seconds=self._summary.duration)

    @property
    def distance(self) -> float:
        """The total distance covered.

        Returns
        -------
            float: Distance covered in the selected metric
        """
        return convert_distance(self._metric, "km", self._summary.length / 1000.0)

    @property
    def ev_duration(self) -> Optional[timedelta]:
        """The total time driving using EV.

        Returns
        -------
            timedelta: The amount of time driving using EV or None if not supported
        """
        return timedelta(seconds=self._hdc.ev_time) if self._hdc else None

    @property
    def ev_distance(self) -> Optional[float]:
        """The total time distance driven using EV.

        Returns
        -------
            timedelta: The distance driven using EV in selected metric or None if not supported
        """
        return (
            convert_distance(self._metric, "km", self._hdc.ev_distance / 1000.0)
            if self._hdc
            else None
        )

    @property
    def from_date(self) -> date:
        """The date the summary started.

        Returns
        -------
            date:         The date the summary started
        """
        return self._from_date

    @property
    def to_date(self) -> date:
        """The date the summary ended.

        Returns
        -------
            date:         The date the summary ended
        """
        return self._to_date

    @property
    def fuel_consumed(self) -> float:
        """The amount of fuel consumed.

        Returns
        -------
            float: The fuel consumed in liters if metric or gallons
        """
        if self._summary.fuel_consumption:
            return (
                round(self._summary.fuel_consumption / 4546.0, 3)
                if self._metric
                else (self._summary.fuel_consumption / 1000.0)
            )

        return 0.0
