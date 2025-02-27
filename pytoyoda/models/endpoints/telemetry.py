"""Toyota Connected Services API - Telemetry Models."""
from datetime import datetime
from typing import Optional

from pydantic.v1 import Field

from pytoyoda.models.endpoints.common import StatusModel, UnitValueModel
from pytoyoda.utils.models import CustomBaseModel


class TelemetryModel(CustomBaseModel):
    r"""Model representing telemetry data.

    Attributes
    ----------
        fuel_type (str): The type of fuel.
        odometer (UnitValueModel): The odometer reading.
        fuel_level (Optional[int]): The fuel level.
        distance_to_empty (Optional[UnitValueModel], optional): The estimated distance to empty. \n
            Defaults to None.
        timestamp (datetime): The timestamp of the telemetry data.

    """

    fuel_type: Optional[str] = Field(alias="fuelType")
    odometer: Optional[UnitValueModel]
    fuel_level: Optional[int] = Field(alias="fuelLevel", default=None)
    distance_to_empty: Optional[UnitValueModel] = Field(alias="distanceToEmpty", default=None)
    timestamp: Optional[datetime]


class TelemetryResponseModel(StatusModel):
    """Model representing a telemetry response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[TelemetryModel], optional): The telemetry payload. Defaults to None.

    """

    payload: Optional[TelemetryModel] = None
