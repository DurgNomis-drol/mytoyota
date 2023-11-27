from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from mytoyota.utils.logs import censor_string


class _VehicleLocationModel(BaseModel):
    displayName: str
    locationAcquisitionDatetime: datetime
    latitude: float
    longitude: float


class LocationModel(BaseModel):
    lastTimestamp: Optional[datetime] = None
    vehicleLocation: Optional[_VehicleLocationModel] = None
    vin: Optional[str] = None

    @field_validator("vin")
    def censor_vin(cls, v):
        v = censor_string(v)
        return v
