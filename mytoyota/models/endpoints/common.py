""" Toyota Connected Services API - Commend Endpoint Models """
from typing import List, Optional, Union

from pydantic import BaseModel, Field


class UnitValueModel(BaseModel):
    unit: str
    value: float


class _MessageModel(BaseModel):
    description: str
    detailed_description: Optional[str] = Field(
        alias="detailedDescription", default=None
    )
    response_code: str = Field(alias="responseCode")


class _MessagesModel(BaseModel):
    messages: List[_MessageModel]


class StatusModel(BaseModel):
    status: Union[str, _MessagesModel]
    code: Optional[int] = None
    errors: Optional[List] = []
    message: Optional[str] = None
