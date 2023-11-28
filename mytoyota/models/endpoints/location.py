""" Toyota Connected Services API - V1 Location Models """
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel

# pylint: disable=locally-disabled, missing-class-docstring, fixme


class _VehicleLocationModel(BaseModel):
    display_name: str = Field(alias="displayName")
    latitude: float
    location_acquisition_datetime: datetime = Field(alias="locationAcquisitionDatetime")
    longitude: float


class LocationModel(BaseModel):
    last_timestamp: Optional[datetime] = Field(alias="lastTimestamp", default=None)
    vehicle_location: Optional[_VehicleLocationModel] = Field(
        alias="vehicleLocation", default=None
    )
    vin: Optional[str] = None


class LocationResponseModel(StatusModel):
    payload: Optional[LocationModel] = None
