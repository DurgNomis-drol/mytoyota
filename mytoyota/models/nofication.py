from datetime import datetime

from mytoyota.models.data import VehicleData


class Notification(VehicleData):
    # TODO Convert category into enum?

    @property
    def category(self) -> str:
        return self._data.get("category", "Unknown")

    @property
    def is_read(self) -> bool:
        return self._data["isRead"] is True

    @property
    def message(self) -> str:
        return self._data["message"]

    @property
    def type(self) -> str:
        return self._data["type"]

    @property
    def date(self) -> datetime:
        return datetime.fromisoformat(self._data["notificationDate"].replace("Z", "+00:00"))
