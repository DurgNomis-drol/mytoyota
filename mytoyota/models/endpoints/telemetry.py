from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from mytoyota.models.endpoints.common import StatusModel, UnitValueModel


class TelemetryModel(BaseModel):
    fuelType: str
    odometer: UnitValueModel
    fuelLevel: int
    distanceToEmpty: UnitValueModel
    timestamp: datetime


class TelemetryResponceModel(StatusModel):
    payload: Optional[TelemetryModel] = None
