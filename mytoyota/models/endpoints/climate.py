"""Toyota Connected Services API - Climate Settings Models."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel, UnitValueModel


class ACParameters(BaseModel):
    """
    Note: Some values are optional as model is also used for SETTING(i.e. Putting) the model
    """
    available: Optional[bool] = None
    display_name: Optional[str] = Field(alias="displayName")
    enabled: bool = False
    icon_url: Optional[str] = Field(alias="iconUrl", default=None)
    name: str


class ACOperations(BaseModel):
    """
    Note: Some values are optional as model is also used for SETTING(i.e. Putting) the model
    """
    available: Optional[bool] = None
    category_display_name: Optional[str] = Field(alias="categoryDisplayName", default=None)
    category_name: str = Field(alias="categoryName")
    ac_parameters: List[ACParameters] = Field(alias="acParameters")


class ClimateSettingsModel(BaseModel):
    """
    Note: Some values are optional as model is also used for SETTING(i.e. Putting) the model
    """
    ac_operations: List[ACOperations] = Field(alias="acOperations")
    max_temp: Optional[float] = Field(alias="maxTemp", default = None)
    min_temp: Optional[float] = Field(alias="minTemp", default=None)
    settings_on: bool = Field(alias="settingsOn")
    temp_interval: Optional[float] = Field(alias="tempInterval", default=None)
    temperature: int
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
