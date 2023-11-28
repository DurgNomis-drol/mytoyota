from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from mytoyota.models.endpoints.common import StatusModel


class _OdometerModel(BaseModel):
    value: int
    unit: str


class _DistanceToEmptyModel(BaseModel):
    value: int
    unit: str


class TelemetryModel(BaseModel):
    fuelType: str
    odometer: _OdometerModel
    fuelLevel: int
    distanceToEmpty: _DistanceToEmptyModel
    timestamp: datetime


class TelemetryResponceModel(StatusModel):
    payload: Optional[TelemetryModel] = None
