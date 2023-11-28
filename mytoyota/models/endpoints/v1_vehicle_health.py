""" Toyota Connected Services API - Endpoint Model """
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel

# pylint: disable=locally-disabled, missing-class-docstring, fixme


class _VehicleHealthModel(BaseModel):
    quantityOfEngOilIcon: Optional[List[Any]] = Field(
        alias="quantityOfEngOilIcon"
    )  # TODO unsure what this returns
    vin: str
    warning: Optional[List[Any]]  # TODO unsure what this returns
    wng_last_upd_time: datetime = Field(alias="wnglastUpdTime")


class V1VehicleHealthModel(StatusModel):
    payload: Optional[_VehicleHealthModel] = None
