"""Toyota Connected Services API - Common Endpoint Models."""
from typing import List, Optional, Union

from pydantic.v1 import Field

from mytoyota.utils.models import CustomBaseModel


class UnitValueModel(CustomBaseModel):
    """Model representing a unit and a value.

    Can be reused several times within other models.

    Attributes
    ----------
        unit (str): The unit of measurement.
        value (float): The numerical value.

    """

    unit: Optional[str] = None
    value: Optional[float] = None


class _MessageModel(CustomBaseModel):
    description: Optional[str]
    detailed_description: Optional[str] = Field(alias="detailedDescription", default=None)
    response_code: Optional[str] = Field(alias="responseCode")


class _MessagesModel(CustomBaseModel):
    messages: Optional[List[_MessageModel]]


class StatusModel(CustomBaseModel):
    """Model representing the status of an endpoint.

    Attributes
    ----------
        status (Union[str, _MessagesModel]): The status of the endpoint,
            which can be a string or a _MessagesModel object.
        code (Optional[int], optional): The status code. Defaults to None.
        errors (Optional[List], optional): A list of errors. Defaults to an empty list.
        message (Optional[str], optional): A message associated with the status. Defaults to None.

    """

    status: Optional[Union[str, _MessagesModel]]
    code: Optional[int] = None
    errors: Optional[List] = None
    message: Optional[str] = None
