""" models for vehicle lock/unlock requests and responses """
from datetime import datetime

from mytoyota.const import UNLOCK_TIMESTAMP_FORMAT
from mytoyota.models.data import VehicleData


class VehicleLockUnlockActionResponse(VehicleData):
    """Model of the response to a Vehicle Lock/Unlock Action Request."""

    @property
    def status(self) -> str:
        """Request Status."""
        return self._data.get("status", "")

    @property
    def request_id(self) -> str:
        """Request ID."""
        return self._data.get("id", "")

    @property
    def type(self) -> str:
        """Request Type."""
        return self._data.get("type", "")


class VehicleLockUnlockStatusResponse(VehicleData):
    """Model of the response to a the request of the status of
    a Vehicle Lock/Unlock action."""

    @property
    def status(self) -> str:
        """Request Status."""
        return self._data.get("status", "")

    @property
    def request_id(self) -> str:
        """Request ID."""
        return self._data.get("id", "")

    @property
    def type(self) -> str:
        """Request Type."""
        return self._data.get("type", "")

    @property
    def request_timestamp(self) -> datetime:
        """Request Timestamp."""
        raw_datetime = self._data.get("requestTimestamp")
        return datetime.strptime(raw_datetime, UNLOCK_TIMESTAMP_FORMAT)
