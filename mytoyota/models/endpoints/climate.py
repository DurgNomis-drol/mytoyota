"""Toyota Connected Services API - Climate Settings Models."""

from datetime import datetime
from typing import List, Optional

from pydantic.v1 import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel, UnitValueModel


class ACParameters(BaseModel):
    """Model representing parameters for AC."""

    available: Optional[bool] = None
    display_name: Optional[str] = Field(alias="displayName")
    enabled: bool = False
    icon_url: Optional[str] = Field(alias="iconUrl", default=None)
    name: str


class ACOperations(BaseModel):
    """Model representing AC operations."""

    available: Optional[bool] = None
    category_display_name: Optional[str] = Field(
        alias="categoryDisplayName", default=None
    )
    category_name: str = Field(alias="categoryName")
    ac_parameters: List[ACParameters] = Field(alias="acParameters")


class ClimateSettingsModel(BaseModel):
    """Model representing climate settings."""

    ac_operations: Optional[List[ACOperations]] = Field(alias="acOperations")
    max_temp: Optional[float] = Field(alias="maxTemp", default=None)
    min_temp: Optional[float] = Field(alias="minTemp", default=None)
    settings_on: bool = Field(alias="settingsOn")
    temp_interval: Optional[float] = Field(alias="tempInterval", default=None)
    temperature: int
    temperature_unit: str = Field(alias="temperatureUnit")


class CurrentTemperature(UnitValueModel):
    """Model representing current temperature."""

    timestamp: datetime


class ClimateOptions(BaseModel):
    """Model representing climate options."""

    front_defogger: bool = Field(alias="frontDefogger")
    rear_defogger: bool = Field(alias="rearDefogger")


class ClimateStatusModel(BaseModel):
    """Model representing climate status."""

    current_temperature: Optional[CurrentTemperature] = Field(
        alias="currentTemperature"
    )
    duration: Optional[int]
    options: Optional[ClimateOptions]
    started_at: Optional[datetime] = Field(alias="startedAt")
    status: bool
    target_temperature: Optional[UnitValueModel] = Field(alias="targetTemperature")
    type: str


class RemoteHVACModel(BaseModel):
    """Model representing remote HVAC."""

    engine_start_time: int = Field(alias="engineStartTime")


class ClimateControlModel(BaseModel):
    """Model representing climate control."""

    command: str
    remote_hvac: Optional[RemoteHVACModel] = Field(alias="remoteHvac", default=None)


class ClimateSettingsResponseModel(StatusModel):
    """Model representing climate settings response."""

    payload: Optional[ClimateSettingsModel] = None


class ClimateStatusResponseModel(StatusModel):
    """Model representing climate status response."""

    payload: Optional[ClimateStatusModel] = None
