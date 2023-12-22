"""models for vehicle notifications."""
from datetime import datetime
from typing import Optional

from mytoyota.models.endpoints.notifications import NotificationModel


class Notification:
    """Notification."""

    def __init__(self, notification: NotificationModel):
        """Initialise Notification."""
        self._notification = notification

    def __repr__(self):
        """Representation of the model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def category(self) -> str:
        """Category of notification.

        For example, ChargingAlert, RemoteCommand

        Returns
        -------
            str: Category of notification
        """
        return self._notification.category

    @property
    def read(self) -> Optional[datetime]:
        """Notification has been read.

        Returns
        -------
            datetime: Time notification read. None if not read.

        """
        return self._notification.read_timestamp

    @property
    def message(self) -> str:
        """Notification message.

        Returns
        -------
            str: Notification message

        """
        return self._notification.message

    @property
    def type(self) -> str:
        """Type.

        For example, Alert

        Returns
        -------
            str: Notification type
        """
        return self._notification.type

    @property
    def date(self) -> datetime:
        """Notification Date.

        Returns
        -------
            datime: Time of notification
        """
        return self._notification.notification_date
