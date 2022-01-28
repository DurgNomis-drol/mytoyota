"""Models for vehicle sensors."""
from __future__ import annotations
from typing import Any

from mytoyota.models.data import VehicleData

def get_attr_in_dict(data: dict[str, float], attr: str) -> float | None:
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
    def current_temperature(self) -> float | None:
        if self.legacy:
            return self._data.get("InsideTemperature")
        return get_attr_in_dict(self._data.get("currentTemperatureIndication", {}), "value")
    
    @property
    def target_temperature(self) -> float | None:
        if self.legacy:
            return self._data.get("SettingTemperature")
        return get_attr_in_dict(self._data.get("targetTemperature", {}), "value")
    
    @property
    def started_at(self) -> str | None:
        if self.legacy:
            return None
        return self._data.get("startedAt")
    
    @property
    def status(self) -> str | None:
        if self.legacy:
            return None
        return self._data.get("status")
    
    @property
    def type(self) -> str | None:
        if self.legacy:
            return None
        return self._data.get("type")
    
    @property
    def duration(self) -> str | None:
        if self.legacy:
            return None
        return self._data.get("duration")
    
    @property
    def options(self) -> dict | list | None:
        if self.legacy:
            return None
        return self._data.get("options")
    
    @property
    def command_id(self) -> str | int | None:
        if self.legacy:
            return None
        return self._data.get("commandId")
    
    @property
    def front_defogger_is_on(self) -> bool | None:
        if self.legacy:
            return self._data.get("FrontDefoggerStatus") == 1
        return None
    
    @property
    def rear_defogger_is_on(self) -> bool | None:
        if self.legacy:
            return self._data.get("RearDefoggerStatus") == 1
        return None

    @property
    def blower_on(self) -> int | None:
        if self.legacy:
            return self._data.get("BlowerStatus")
        return None
    
    @property
    def last_updated(self) -> str | None:
        if self.legacy:
            return None
        return get_attr_in_dict(self._data.get("currentTemperatureIndication", {}), "timestamp")