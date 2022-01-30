"""Models for vehicle sensors."""
from __future__ import annotations

from typing import TYPE_CHECKING

from mytoyota.utils.conversions import convert_to_miles

if TYPE_CHECKING:
    from mytoyota.models.vehicle import Vehicle


class Dashboard:
    """Instrumentation data model."""

    def __init__(
        self,
        vehicle: Vehicle,
    ) -> None:
        """Dashboard."""
        self._vehicle = vehicle

        vehicle_info = vehicle._status_legacy.get("VehicleInfo", {})
        self._chargeinfo = vehicle_info.get("ChargeInfo", {})
        self._energy = (
            vehicle._status.get("energy", [])[0] if "energy" in vehicle._status else {}
        )

    @property
    def legacy(self) -> bool:
        """If the car uses the legacy endpoints."""
        if "Fuel" in self._vehicle.odometer:
            return True
        return False

    @property
    def is_metric(self) -> bool:
        """If the car is reporting data in metric."""
        return self._vehicle.odometer.get("mileage_unit") == "km"

    @property
    def odometer(self) -> int | None:
        """Shows the odometer distance."""
        return self._vehicle.odometer.get("mileage")

    @property
    def fuel_level(self) -> float | None:
        """Shows the fuellevel of the vehicle."""
        if self.legacy:
            return self._vehicle.odometer.get("Fuel")
        return self._energy.get("level")

    @property
    def fuel_range(self) -> float | None:
        """Shows the range if available."""
        fuel_range = (
            self._chargeinfo.get("GasolineTravelableDistance")
            if self.legacy
            else self._energy.get("remainingRange", None)
        )
        return convert_to_miles(fuel_range) if not self.is_metric else fuel_range

    @property
    def battery_level(self) -> float | None:
        """Shows the battery level if a hybrid."""
        if self.legacy:
            return self._chargeinfo.get("ChargeRemainingAmount")
        return None

    @property
    def battery_range(self) -> float | None:
        """Shows the battery range if a hybrid."""
        if self.legacy:
            battery_range = self._chargeinfo.get("EvDistanceInKm")
            return (
                convert_to_miles(battery_range) if not self.is_metric else battery_range
            )
        return None

    @property
    def battery_range_with_aircon(self) -> float | None:
        """Shows the battery range with aircon on, if a hybrid."""
        if self.legacy:
            battery_range = self._chargeinfo.get("EvDistanceWithAirCoInKm")
            return (
                convert_to_miles(battery_range) if not self.is_metric else battery_range
            )
        return None

    @property
    def charging_status(self) -> str | None:
        """Shows the charging status if a hybrid."""
        if self.legacy:
            return self._chargeinfo.get("ChargingStatus")
        return None

    @property
    def remaining_charge_time(self) -> int | None:
        """Shows the remaining time to a full charge, if a hybrid."""
        if self.legacy:
            return self._chargeinfo.get("RemainingChargeTime")
        return None
