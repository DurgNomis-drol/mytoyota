"""Models for vehicle sensors."""
from __future__ import annotations
from typing import Any

from mytoyota.utils.conversions import convert_to_miles


class Dashboard:
    """Instrumentation data model."""

    _chargeinfo: dict[str, Any]
    _energy: dict[str, Any]

    def __init__(
        self,
        vehicle,
        ) -> None:
        self._vehicle = vehicle

        vehicle_info = vehicle._status_legacy.get("VehicleInfo", {})
        self._chargeinfo = vehicle_info.get("ChargeInfo", {})
        self._energy = vehicle._status.get("energy", [])[0] if vehicle._status.get("energy") else {}

    @property
    def legacy(self) -> bool:
        if "Fuel" in self._vehicle._odometer:
            return True
        return False
    
    @property
    def is_metric(self) -> bool:
        return self._vehicle._odometer.get("mileage_unit") == "km"
    
    @property
    def odometer(self) -> int | None:
        return self._vehicle._odometer.get("mileage")
    
    @property
    def fuel_level(self) -> float | None:
        if self.legacy:
            return self._vehicle._odometer.get("Fuel")
        return self._energy.get("level")
    
    @property
    def range(self) -> float | None:
        range = (
            self._chargeinfo.get("GasolineTravelableDistance") 
            if self.legacy 
            else self._energy.get("remainingRange", None)
        )
        return convert_to_miles(range) if not self.is_metric else range
    
    @property
    def battery_level(self) -> float | None:
        if self.legacy:
            return self._chargeinfo.get("ChargeRemainingAmount")
        return None
    
    @property
    def battery_range(self) -> float | None:
        if self.legacy:
            range = self._chargeinfo.get("EvDistanceInKm")
            return convert_to_miles(range) if not self.is_metric else range
        return None
    
    @property
    def battery_range_with_aircon(self) -> float | None:
        if self.legacy:
            range = self._chargeinfo.get("EvDistanceWithAirCoInKm")
            return convert_to_miles(range) if not self.is_metric else range
        return None
    
    @property
    def charging_status(self) -> str | None:
        if self.legacy:
            return self._chargeinfo.get("ChargingStatus")
        return None
    
    @property
    def remaining_charge_time(self) -> int | None:
        if self.legacy:
            return self._chargeinfo.get("RemainingChargeTime")
        return None
    