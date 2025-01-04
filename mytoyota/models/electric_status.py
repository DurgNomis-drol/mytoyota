"""models for vehicle electric status."""
from datetime import date
from typing import Optional

from mytoyota.models.endpoints.electric import ElectricStatusModel
from mytoyota.utils.conversions import convert_distance


class ElectricStatus:
    """ElectricStatus."""

    def __init__(
        self,
        electric_status: ElectricStatusModel = None,
        metric: bool = True,
    ):
        """Initialise ElectricStatus."""
        self._electric_status: Optional[ElectricStatusModel] = (
            electric_status.payload if electric_status else None
        )
        self._distance_unit: str = "km" if metric else "mi"

    def __repr__(self):
        """Representation of the model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def battery_level(self) -> Optional[float]:
        """Battery level of the vehicle.

        Returns
        -------
            float: Battery level of the vehicle in percentage.

        """
        return self._electric_status.battery_level if self._electric_status else None

    @property
    def charging_status(self) -> Optional[str]:
        """Charging status of the vehicle.

        Returns
        -------
            str: Charging status of the vehicle.

        """
        return self._electric_status.charging_status

    @property
    def remaining_charge_time(self) -> Optional[int]:
        """Remaining time to full charge in minutes.

        Returns
        -------
            int: Remaining time to full charge in minutes.

        """
        return self._electric_status.remaining_charge_time

    @property
    def ev_range(self) -> Optional[float]:
        """Electric vehicle range.

        Returns
        -------
            float: Electric vehicle range in the current selected units.

        """
        if self._electric_status:
            return convert_distance(
                self._distance_unit,
                self._electric_status.ev_range.unit,
                self._electric_status.ev_range.value,
            )
        return None

    @property
    def ev_range_with_ac(self) -> Optional[float]:
        """Electric vehicle range with AC.

        Returns
        -------
            float: Electric vehicle range with AC in the current selected units.

        """
        if self._electric_status:
            return convert_distance(
                self._distance_unit,
                self._electric_status.ev_range_with_ac.unit,
                self._electric_status.ev_range_with_ac.value,
            )
        return None

    @property
    def can_set_next_charging_event(self) -> Optional[bool]:
        """Can set next charging event.

        Returns
        -------
            bool: Can set next charging event.

        """
        return self._electric_status.can_set_next_charging_event if self._electric_status else None

    @property
    def last_update_timestamp(self) -> Optional[date]:
        """Last update timestamp.

        Returns
        -------
            date: Last update timestamp.

        """
        return self._electric_status.last_update_timestamp if self._electric_status else None
