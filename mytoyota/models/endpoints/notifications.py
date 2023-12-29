"""Toyota Connected Services API - Notification Models."""
from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field


class _HeadersModel(BaseModel):
    content_type: str = Field(..., alias="Content-Type")


class NotificationModel(BaseModel):
    """Model representing a notification.

    Attributes
    ----------
        message_id (str): The ID of the notification message.
        vin (str): The VIN (Vehicle Identification Number) associated with the notification.
        notification_date (datetime): The datetime of the notification.
        is_read (bool): Indicates whether the notification has been read.
        read_timestamp (datetime): The timestamp when the notification was read.
        icon_url (str): The URL of the notification icon.
        message (str): The content of the notification message.
        status (Union[int, str]): The status of the notification.
        type (str): The type of the notification.
        category (str): The category of the notification.
        display_category (str): The display category of the notification.

    """

    message_id: str = Field(alias="messageId")
    vin: str
    notification_date: datetime = Field(alias="notificationDate")
    is_read: bool = Field(alias="isRead")
    read_timestamp: Optional[datetime] = Field(alias="readTimestamp", default=None)
    icon_url: str = Field(alias="iconUrl")
    message: str
    status: Optional[Union[int, str]] = None
    type: str
    category: str
    display_category: str = Field(alias="displayCategory")


class _PayloadItemModel(BaseModel):
    vin: str
    notifications: List[NotificationModel]


class NotificationResponseModel(BaseModel):
    r"""Model representing a notification response.

    Attributes
    ----------
        guid (UUID): The GUID (Globally Unique Identifier) of the response.
        status_code (int): The status code of the response.
        headers (_HeadersModel): The headers of the response.
        body (str): The body of the response.
        payload (Optional[List[_PayloadItemModel]], optional): The payload of the response. \n
            Defaults to None.

    """

    guid: UUID
    status_code: int = Field(alias="statusCode")
    headers: _HeadersModel
    body: str
    payload: Optional[List[_PayloadItemModel]] = None
