""" Toyota Connected Services API - Endpoint Model """
from datetime import datetime
from typing import Any, Optional, List, Union
from pydantic import BaseModel, Field

from .common import StatusModel

# pylint: disable=locally-disabled, missing-class-docstring, fixme


class VehicleHealthModel(BaseModel):
    quantityOfEngOilIcon: Optional[List[Any]] = Field(
        alias="quantityOfEngOilIcon"
    )  # TODO unsure what this returns
    vin: str
    warning: Optional[List[Any]]  # TODO unsure what this returns
    wng_last_upd_time: datetime = Field(alias="wnglastUpdTime")


class VehicleHealthResponseModel(BaseModel):
    code: Optional[int] = None  # HTML Status code
    errors: Optional[List[Any]] = None  # TODO unsure what this returns
    payload: Optional[VehicleHealthModel] = None
    status: Union[str, StatusModel]
