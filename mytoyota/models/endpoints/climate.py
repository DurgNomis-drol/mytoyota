"""Toyota Connected Services API - Climate Settings Models."""
from datetime import datetime
from typing import List, Optional
from uuid import UUID


from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel


class ACParameters(BaseModel):
    available: bool
    display_name: List[str] = Field(alias="displayName")
    icon_url: str = Field(alias="iconUrl")
    name: str


class _ClimateSettingsModel(BaseModel):
    ac_operations: List[ACParameters] = Field(alias="acOperations")
    max_temp: float = Field(alias="maxTemp")
    min_temp: float = Field(alias="minTemp")
    settings_on: bool = Field(alias="settingsOn")
    temp_interval: float = Field(alias="tempInterval")
    temperature: float
    temperature_unit: str = Field(alias="temperatureUnit")


class ClimateSettingsResponseModel(StatusModel):
    payload: _ClimateSettingsModel