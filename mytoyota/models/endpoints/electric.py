""" Toyota Connected Services API - Electric Models """
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel, _Range

# pylint: disable=locally-disabled, missing-class-docstring, fixme


class ElectricStatusModel(BaseModel):
    battery_level: int = Field(alias="batteryLevel")
    can_set_next_charging_event: bool = Field(alias="canSetNextChargingEvent")
    charging_status: str = Field(alias="chargingStatus")
    ev_range: _Range = Field(alias="evRange")
    ev_range_with_ac: _Range = Field(alias="evRangeWithAc")
    fuel_level: int = Field(alias="fuelLevel")
    fuel_range: _Range = Field(alias="fuelRange")
    last_update_timestamp: datetime = Field(alias="lastUpdateTimestamp")


class ElectricResponseModel(StatusModel):
    payload: Optional[ElectricStatusModel] = None
