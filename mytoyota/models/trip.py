"""Models for trips and detailed trips."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

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
    def trip_events(self) -> List[TripEvent]:
        """Trip events."""
        return (
            [TripEvent(event) for event in self._data.get("tripEvents", [])]
            if self._data.get("tripEvents")
            else []
        )

    @property
    def trip_events_type(self) -> List[Dict]:
        """Trip events type."""
        return self._data.get("tripEventsType", [])

    @property
    def statistics(self) -> Dict:
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
    def start_time_gmt(self) -> Optional[datetime]:
        """Trip Start time GMT."""
        start_time_str = self._data.get("startTimeGmt", None)
        return (
            datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%SZ")
            if start_time_str
            else None
        )

    @property
    def end_time_gmt(self) -> Optional[datetime]:
        """Trip End time GMT."""
        end_time_str = self._data.get("endTimeGmt", None)
        return (
            datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%SZ")
            if end_time_str
            else None
        )

    @property
    def end_address(self) -> str:
        """End address."""
        return self._data.get("endAddress", "")

    @property
    def classification_type(self) -> Optional[int]:
        """Trip Classification type."""
        return self._data.get("classificationType", None)
