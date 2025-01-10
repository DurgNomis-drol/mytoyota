"""Toyota Connected Services API - Notification Models."""
from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic.v1 import Field

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

    message_id: Optional[str] = Field(alias="messageId")
    vin: Optional[str]
    notification_date: Optional[datetime] = Field(alias="notificationDate")
    is_read: Optional[bool] = Field(alias="isRead")
    read_timestamp: Optional[datetime] = Field(alias="readTimestamp", default=None)
    icon_url: Optional[str] = Field(alias="iconUrl")
    message: Optional[str]
    status: Optional[Union[int, str]] = None
    type: Optional[str]
    category: Optional[str]
    display_category: Optional[str] = Field(alias="displayCategory")


class _PayloadItemModel(CustomBaseModel):
    vin: Optional[str] = None
    notifications: Optional[List[NotificationModel]]


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
    status_code: Optional[int] = Field(alias="statusCode")
    headers: Optional[_HeadersModel]
    body: Optional[str]
    payload: Optional[List[_PayloadItemModel]] = None
