""" Toyota Connected Services API - Notification Models """
from datetime import datetime
from pydantic import BaseModel, Field

from .common import StatusModel

# pylint: disable=locally-disabled, missing-class-docstring, fixme


class NotificationModel(BaseModel):
    message_id: str = Field(alias="messageId")
    vin: str
    notification_date: datetime = Field(alias="notificationDate")
    is_read: bool = Field(alias="isRead")
    read_timestamp: datetime = Field(alias="readTimestamp")
    icon_url: str = Field(alias="iconUrl")
    message: str
    status: int
    type: str
    category: str
    display_category: str = Field(alias="displayCategory")


class NotificationResponse(BaseModel):
    payload: NotificationModel
    status: StatusModel
