"""Toyota Connected Services API - Climate Settings Models."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel, UnitValueModel


class ACParameters(BaseModel):
    available: bool
    display_name: List[str] = Field(alias="displayName")
    enabled: Optional[bool] = False
    icon_url: str = Field(alias="iconUrl")
    name: str


class ACOperations(BaseModel):
    available: bool
    category_display_name: str = Field(alias="categoryDisplayName")
    category_name: str = Field(alias="categoryName")


# class PutACOperations(BaseModel):
#    ac_parameters


class ClimateSettingsModel(BaseModel):
    ac_operations: List[ACOperations] = Field(alias="acOperations")
    max_temp: float = Field(alias="maxTemp")
    min_temp: float = Field(alias="minTemp")
    settings_on: bool = Field(alias="settingsOn")
    temp_interval: float = Field(alias="tempInterval")
    temperature: float
    temperature_unit: str = Field(alias="temperatureUnit")


class _CurrentTemperature(UnitValueModel):
    timestamp: datetime


class _ClimateOptions(BaseModel):
    front_defogger: bool = Field(alias="frontDefogger")
    rear_defogger: bool = Field(alias="rearDefogger")


class _ClimateStatusModel(BaseModel):
    current_temperature: Optional[_CurrentTemperature] = Field(alias="currentTemperature")
    duration: Optional[int]
    options: Optional[_ClimateOptions]
    started_at: Optional[datetime] = Field(alias="startedAt")
    status: bool
    target_temperature: Optional[UnitValueModel]
    type: str


class ClimateControlModel(BaseModel):
    command: str


class ClimateSettingsResponseModel(StatusModel):
    payload: ClimateSettingsModel


class ClimateStatusResponseModel(StatusModel):
    payload: _ClimateStatusModel
