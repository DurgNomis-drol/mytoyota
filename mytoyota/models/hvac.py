"""Models for vehicle sensors."""
from __future__ import annotations

from typing import Any, Optional, Union

from mytoyota.models.data import VehicleData


def get_attr_in_dict(data: dict[str, float], attr: str) -> float | None:
    """Get a specific attribute from a dict"""
    return data.get(attr)


class Hvac(VehicleData):
    """HVAC data model."""

    def __init__(self, data: dict[str, Any], legacy: bool = False) -> None:
        # Support legacy method. Toyota seems to be changing their api for newer
        # cars, though not a lot seems to use the method yet.
        # This option enables support for older cars.
        super().__init__(data)
        self.legacy = legacy

    @property
    def current_temperature(self) -> Optional[float]:
        """Current temperature."""
        if self.legacy:
            return self._data.get("InsideTemperature")
        return get_attr_in_dict(
            self._data.get("currentTemperatureIndication", {}), "value"
        )

    @property
    def target_temperature(self) -> Optional[float]:
        """Target temperature."""
        if self.legacy:
            return self._data.get("SettingTemperature")
        return get_attr_in_dict(self._data.get("targetTemperature", {}), "value")

    @property
    def started_at(self) -> Optional[str]:
        """Hvac started at."""
        return None if self.legacy else self._data.get("startedAt")

    @property
    def status(self) -> Optional[str]:
        """Hvac status."""
        return None if self.legacy else self._data.get("status")

    @property
    def type(self) -> Optional[str]:
        """Hvac type."""
        return None if self.legacy else self._data.get("type")

    @property
    def duration(self) -> Optional[str]:
        """Hvac duration."""
        return None if self.legacy else self._data.get("duration")

    @property
    def options(self) -> Optional[Union[list, dict]]:
        """Hvac options."""
        return None if self.legacy else self._data.get("options")

    @property
    def command_id(self) -> Optional[Union[str, int]]:
        """Hvac command id."""
        return None if self.legacy else self._data.get("commandId")

    @property
    def front_defogger_is_on(self) -> Optional[bool]:
        """If the front defogger is on."""
        return self._data.get("FrontDefoggerStatus") == 1 if self.legacy else None

    @property
    def rear_defogger_is_on(self) -> Optional[bool]:
        """If the rear defogger is on."""
        return self._data.get("RearDefoggerStatus") == 1 if self.legacy else None

    @property
    def blower_on(self) -> Optional[int]:
        """Hvac blower setting."""
        return self._data.get("BlowerStatus") if self.legacy else None

    @property
    def last_updated(self) -> Optional[float]:
        """Hvac last updated."""
        if self.legacy:
            return None
        return get_attr_in_dict(
            self._data.get("currentTemperatureIndication", {}), "timestamp"
        )
