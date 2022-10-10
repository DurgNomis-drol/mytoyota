"""Models for trips and detailed trips."""
from __future__ import annotations

from datetime import datetime

from mytoyota.models.data import VehicleData


class TripEvent(VehicleData):
    """A single trip event including geo location."""

    @property
    def latitude(self) -> float:
        """Event latitude."""
        return float(self._data.get("lat", 0.0))

    @property
    def longitude(self) -> float:
        """Event longitude."""
        return float(self._data.get("lon", 0.0))

    @property
    def overspeed(self) -> bool:
        """Overspeed notice"""
        return bool(self._data.get("overspeed", False))

    @property
    def highway(self) -> bool:
        """Highway."""
        return bool(self._data.get("highway", False))

    @property
    def is_ev(self) -> bool:
        """Running in ev mode"""
        return bool(self._data.get("isEv", False))

    @property
    def mode(self) -> int:
        """Mode"""
        return int(self._data.get("mode", 0))


class DetailedTrip(VehicleData):
    """Detailed Trip model."""

    @property
    def trip_events(self) -> list(TripEvent):
        """Trip events."""
        if not self._data.get("tripEvents"):
            return []
        return [TripEvent(event) for event in self._data.get("tripEvents", [])]

    @property
    def trip_events_type(self) -> list(dict):
        """Trip events type."""
        return self._data.get("tripEventsType", [])

    @property
    def statistics(self) -> dict:
        """Statistics."""
        return self._data.get("statistics", {})


class Trip(VehicleData):
    """Trip model. returned by get-trips()"""

    @property
    def trip_id(self) -> str:
        """Trip ID."""
        return self._data.get("tripId", "")

    @property
    def start_address(self) -> str:
        """Start address."""
        return self._data.get("startAddress", "")

    @property
    def start_time_gmt(self) -> datetime.datetime | None:
        """Trip Start time GMT."""
        start_time_str = self._data.get("startTimeGmt", None)
        if not start_time_str:
            return None
        return datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%SZ")

    @property
    def end_time_gmt(self) -> datetime.datetime | None:
        """Trip End time GMT."""
        end_time_str = self._data.get("endTimeGmt", None)
        if not end_time_str:
            return None
        return datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%SZ")

    @property
    def end_address(self) -> str:
        """End address."""
        return self._data.get("endAddress", "")

    @property
    def classification_type(self) -> int | None:
        """Trip Classification type."""
        return self._data.get("classificationType", None)
