"""Toyota Connected Services API - Telemetry Models."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel, UnitValueModel


class TelemetryModel(BaseModel):
    r"""Model representing telemetry data.

    Attributes
    ----------
        fuel_type (str): The type of fuel.
        odometer (UnitValueModel): The odometer reading.
        fuel_level (int): The fuel level.
        distance_to_empty (Optional[UnitValueModel], optional): The estimated distance to empty. \n
            Defaults to None.
        timestamp (datetime): The timestamp of the telemetry data.

    """

    fuel_type: str = Field(alias="fuelType")
    odometer: UnitValueModel
    fuel_level: int = Field(alias="fuelLevel")
    distance_to_empty: Optional[UnitValueModel] = Field(alias="distanceToEmpty", default=None)
    timestamp: datetime


class TelemetryResponseModel(StatusModel):
    """Model representing a telemetry response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[TelemetryModel], optional): The telemetry payload. Defaults to None.

    """

    payload: Optional[TelemetryModel] = None
