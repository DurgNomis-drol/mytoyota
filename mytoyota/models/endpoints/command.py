"""Toyota Connected Services API - Climate Settings Models."""

from enum import Enum
from typing import Optional

from pydantic.v1 import BaseModel, Field


class CommandType(str, Enum):
    """List of possible commands."""

    DOOR_LOCK = "door-lock"
    DOOR_UNLOCK = "door-unlock"
    ENGINE_START = "engine-start"
    ENGINE_STOP = "engine-stop"
    HAZARD_ON = "hazard-on"
    HAZARD_OFF = "hazard-off"
    WINDOW_ON = "power-window-on"
    WINDOW_OFF = "power-window-off"
    AC_SETTINGS_ON = "ac-settings-on"
    SOUND_HORN = "sound-horn"
    BUZZER_WARNING = "buzzer-warning"
    FIND_VEHICLE = "find-vehicle"
    VENTILATION_ON = "ventilation-on"
    TRUNK_LOCK = "trunk-lock"
    TRUNK_UNLOCK = "trunk-unlock"
    HEADLIGHT_ON = "headlight-on"
    HEADLIGHT_OFF = "headlight-off"


class RemoteCommandModel(BaseModel):
    """Model representing an remote command."""

    beep_count: Optional[int] = Field(alias="beepCount", default=None)
    command: CommandType

    class Config:
        """Pydantic serialization option for enum value use."""

        use_enum_values = True
