"""Toyota Connected Services API - Notification Models."""
from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic import Field

from mytoyota.utils.models import CustomBaseModel


class _HeadersModel(CustomBaseModel):
    content_type: Optional[str] = Field(..., alias="Content-Type")


class NotificationModel(CustomBaseModel):
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

    message_id: Optional[str] = Field(None, alias="messageId")
    vin: Optional[str] = None
    notification_date: Optional[datetime] = Field(None, alias="notificationDate")
    is_read: Optional[bool] = Field(None, alias="isRead")
    read_timestamp: Optional[datetime] = Field(alias="readTimestamp", default=None)
    icon_url: Optional[str] = Field(None, alias="iconUrl")
    message: Optional[str] = None
    status: Optional[Union[int, str]] = None
    type: Optional[str] = None
    category: Optional[str] = None
    display_category: Optional[str] = Field(None, alias="displayCategory")


class _PayloadItemModel(CustomBaseModel):
    vin: Optional[str] = None
    notifications: Optional[List[NotificationModel]] = None


class NotificationResponseModel(CustomBaseModel):
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

    guid: Optional[UUID] = None
    status_code: Optional[int] = Field(None, alias="statusCode")
    headers: Optional[_HeadersModel] = None
    body: Optional[str] = None
    payload: Optional[List[_PayloadItemModel]] = None
