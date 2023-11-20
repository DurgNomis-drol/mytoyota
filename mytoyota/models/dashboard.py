"""Models for vehicle sensors."""
import logging

from mytoyota.models.data import VehicleData
from mytoyota.utils.conversions import convert_to_miles


class Dashboard(VehicleData):
    """Instrumentation data model."""

    @property
    def is_metric(self) -> bool:
        """If the car is reporting data in metric."""
        # Annoyingly the data is both in imperial & metric.
        # Lets pick imperial
        return False

    @property
    def odometer(self) -> int | None:
        """Shows the odometer distance."""
        if self._data["odometer"]["unit"] == "mi":
            return self._data["odometer"]["value"]

        return convert_to_miles(self._data["odometer"]["value"])

    @property
    def fuel_level(self) -> float | None:
        """Shows the fuellevel of the vehicle."""
        return self._data["fuelLevel"]

    @property
    def fuel_range(self) -> float | None:
        """Shows the range if available."""
        if self._data["fuelRange"]["unit"] == "mi":
            return self._data["odometer"]["value"]

        return convert_to_miles(self._data["fuelRange"]["value"])

    @property
    def battery_level(self) -> float | None:
        """Shows the battery level if a hybrid."""
        if "batteryLevel" in self._data:
            return self._data["batteryLevel"]

        return None

    @property
    def battery_range(self) -> float | None:
        """Shows the battery range if a hybrid."""
        if "evRange" in self._data:
            if self._data["evRange"]["unit"] == "mi":
                return self._data["evRange"]["value"]

            return convert_to_miles(self._data["evRange"]["value"])

        return None

    @property
    def battery_range_with_aircon(self) -> float | None:
        """Shows the battery range with aircon on, if a hybrid."""
        if "evRangeWithAc" in self._data:
            if self._data["evRangeWithAc"]["unit"] == "mi":
                return self._data["evRangeWithAc"]["value"]

            return convert_to_miles(self._data["evRangeWithAc"]["value"])

        return None

    @property
    def charging_status(self) -> str | None:
        """Shows the charging status if a hybrid."""
        if "chargingStatus" in self._data:
            return self._data["chargingStatus"]

        return None

    @property
    def remaining_charge_time(self) -> int | None:
        """Shows the remaining time to a full charge, if a hybrid."""
        # TODO: What units?
        if "remainingChargeTime" in self._data:
            return self._data["remainingChargeTime"]

        return None
