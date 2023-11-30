""" models for vehicle notifications """
from datetime import datetime

from mytoyota.models.data import VehicleData


class Notification(VehicleData):
    """Notification"""

    # TODO Convert category into enum?

    @property
    def category(self) -> str:
        """Category"""
        return self._data.get("category", "Unknown")

    @property
    def is_read(self) -> bool:
        """Is read"""
        return self._data["isRead"] is True

    @property
    def message(self) -> str:
        """Message"""
        return self._data["message"]

    @property
    def type(self) -> str:
        """Type"""
        return self._data["type"]

    @property
    def date(self) -> datetime:
        """Date"""
        return datetime.fromisoformat(self._data["notificationDate"].replace("Z", "+00:00"))
