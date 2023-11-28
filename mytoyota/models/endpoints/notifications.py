""" Toyota Connected Services API - Notification Models """
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

# pylint: disable=locally-disabled, missing-class-docstring, fixme


class _HeadersModel(BaseModel):
    content_type: str = Field(..., alias="Content-Type")


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


class _PayloadItemModel(BaseModel):
    vin: str
    notifications: List[NotificationModel]


class NotificationResponse(BaseModel):
    guid: UUID
    statusCode: int
    headers: _HeadersModel
    body: str
    payload: Optional[List[_PayloadItemModel]] = None
