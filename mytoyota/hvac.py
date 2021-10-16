"""HVAC representation for mytoyota"""


class Hvac:
    """Representation of the HVAC system in the car"""

    legacy: bool = False

    def __init__(self, hvac: dict, legacy: bool = False) -> None:
        # Support legacy method. Toyota seems to be changing their api for newer
        # cars, though not a lot seems to use the method yet.
        # This option enables support for older cars.
        if legacy:
            self._set_legacy(hvac)
        else:
            self._set(hvac)

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return hvac as dict."""
        return vars(self)

    def _set(self, hvac: dict) -> None:
        """Set attributes"""
        current_temp = hvac.get("currentTemperatureIndication", {})
        self.current_temperature = current_temp.get("value", None)
        target_temp = hvac.get("targetTemperature", {})
        self.target_temperature = target_temp.get("value", None)
        self.started_at = hvac.get("startedAt", None)
        self.status = hvac.get("status", None)
        self.type = hvac.get("type", None)
        self.duration = hvac.get("duration", None)

        self.options = hvac.get("options", None)
        self.command_id = hvac.get("commandId", None)

        self.last_updated = current_temp.get("timestamp", None)

    def _set_legacy(self, hvac: dict) -> None:
        """Set attributes using legacy data"""
        self.legacy = True

        self.current_temperature = hvac.get("InsideTemperature", None)
        self.target_temperature = hvac.get("SettingTemperature", None)
        self.blower_on = hvac.get("BlowerStatus", None)

        self.front_defogger_on = hvac.get("FrontDefoggerStatus", False)
        self.rear_defogger_on = hvac.get("RearDefoggerStatus", False)

        self.last_updated = hvac.get("LatestAcStartTime", None)
