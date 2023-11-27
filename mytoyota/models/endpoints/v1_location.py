""" Toyota Connected Services API - V1 Location Models """
from datetime import datetime
from typing import Optional, List, Any, Union
from pydantic import BaseModel, Field

from .common import _StatusModel

# pylint: disable=locally-disabled, missing-class-docstring, fixme


class _VehicleLocationModel(BaseModel):
    display_name: str = Field(alias="displayName")
    latitude: float
    location_acquisition_datetime: datetime = Field(alias="locationAcquisitionDatetime")
    longitude: float


class _LocationModel(BaseModel):
    last_timestamp: Optional[datetime] = Field(alias="lastTimestamp", default=None)
    vehicle_location: Optional[_VehicleLocationModel] = Field(
        alias="vehicleLocation", default=None
    )
    vin: Optional[str] = None


class V1LocationModel(BaseModel):
    code: Optional[int] = None
    errors: Optional[List[Any]] = None  # TODO unsure what this returns
    message: Optional[str] = None
    payload: Optional[_LocationModel] = None
    status: Union[str, _StatusModel]
