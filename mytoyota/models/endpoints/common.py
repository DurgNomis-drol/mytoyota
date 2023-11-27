""" Toyota Connected Services API - Commend Endpoint Models """
from typing import List, Optional
from pydantic import BaseModel, Field


class _MessageModel(BaseModel):
    description: str
    detailed_description: Optional[str] = Field(
        alias="detailedDescription", default=None
    )
    response_code: str = Field(alias="responseCode")


class _StatusModel(BaseModel):
    messages: List[_MessageModel]
