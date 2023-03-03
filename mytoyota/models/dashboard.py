"""Models for vehicle sensors."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mytoyota.utils.conversions import convert_to_miles

if TYPE_CHECKING:
    from mytoyota.models.vehicle import Vehicle  # pragma: no cover


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
        return "Fuel" in self._vehicle.odometer

    @property
    def is_metric(self) -> bool:
        """If the car is reporting data in metric."""
        return self._vehicle.odometer.get("mileage_unit") == "km"

    @property
    def odometer(self) -> Optional[int]:
        """Shows the odometer distance."""
        return self._vehicle.odometer.get("mileage")

    @property
    def fuel_level(self) -> Optional[float]:
        """Shows the fuellevel of the vehicle."""
        if self.legacy:
            return self._vehicle.odometer.get("Fuel")
        return self._energy.get("level")

    @property
    def fuel_range(self) -> Optional[float]:
        """Shows the range if available."""
        fuel_range = (
            self._chargeinfo.get("GasolineTravelableDistance")
            if self.legacy
            else self._energy.get("remainingRange", None)
        )
        if fuel_range is not None:
            return fuel_range if self.is_metric else convert_to_miles(fuel_range)
        return fuel_range

    @property
    def battery_level(self) -> Optional[float]:
        """Shows the battery level if a hybrid."""
        return self._chargeinfo.get("ChargeRemainingAmount") if self.legacy else None

    @property
    def battery_range(self) -> Optional[float]:
        """Shows the battery range if a hybrid."""

        battery_range = self._chargeinfo.get("EvDistanceInKm") if self.legacy else None
        if battery_range is not None:
            battery_range = (
                battery_range if self.is_metric else convert_to_miles(battery_range)
            )

        return battery_range

    @property
    def battery_range_with_aircon(self) -> Optional[float]:
        """Shows the battery range with aircon on, if a hybrid."""
        battery_range = (
            self._chargeinfo.get("EvDistanceWithAirCoInKm") if self.legacy else None
        )
        if battery_range is not None:
            battery_range = (
                battery_range if self.is_metric else convert_to_miles(battery_range)
            )

        return battery_range

    @property
    def charging_status(self) -> Optional[str]:
        """Shows the charging status if a hybrid."""
        return self._chargeinfo.get("ChargingStatus") if self.legacy else None

    @property
    def remaining_charge_time(self) -> Optional[int]:
        """Shows the remaining time to a full charge, if a hybrid."""
        return self._chargeinfo.get("RemainingChargeTime") if self.legacy else None
