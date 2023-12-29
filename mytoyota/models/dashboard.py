"""Models for vehicle sensors."""
from datetime import timedelta
from typing import Any, List, Optional

from mytoyota.models.endpoints.electric import ElectricResponseModel
from mytoyota.models.endpoints.telemetry import TelemetryResponseModel
from mytoyota.models.endpoints.vehicle_health import VehicleHealthResponseModel
from mytoyota.utils.conversions import convert_distance


class Dashboard:
    """Information that may be found on a vehicles dashboard."""

    # TODO do we want to supply last update times?

    def __init__(  # noqa: D417
        self,
        telemetry: Optional[TelemetryResponseModel] = None,
        electric: Optional[ElectricResponseModel] = None,
        health: Optional[VehicleHealthResponseModel] = None,
        metric: bool = True,
    ):
        """Initialise Dashboard.

        Parameters
        ----------
            metric: bool:   Report distances in metric(or imperial)
        """
        self._electric = electric.payload if electric else None
        self._telemetry = telemetry.payload if telemetry else None
        self._health = health.payload if health else None
        self._metric = "km" if metric else "mi"

    def __repr__(self):
        """Representation of the Dashboard model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def odometer(self) -> float:
        """Odometer distance.

        Returns
        -------
            The latest odometer reading in the current selected units
        """
        return convert_distance(
            self._metric, self._telemetry.odometer.unit, self._telemetry.odometer.value
        )

    @property
    def fuel_level(self) -> int:
        """Fuel level.

        Returns
        -------
            A value as percentage
        """
        return self._telemetry.fuel_level

    @property
    def battery_level(self) -> Optional[float]:
        """Shows the battery level if available.

        Returns
        -------
            A value as percentage
        """
        return self._electric.battery_level if self._electric else None

    @property
    def fuel_range(self) -> Optional[float]:
        """The range using _only_ fuel.

        Returns
        -------
            The range in the currently selected unit.

            If vehicle is electric returns 0
            If vehicle doesn't support fuel range returns None
        """
        if self._electric:
            return convert_distance(
                self._metric,
                self._electric.fuel_range.unit,
                self._electric.fuel_range.value,
            )
        if self._telemetry.distance_to_empty:
            return convert_distance(
                self._metric,
                self._telemetry.distance_to_empty.unit,
                self._telemetry.distance_to_empty.value,
            )

        return None

    @property
    def battery_range(self) -> Optional[float]:
        """The range using _only_ EV.

        Returns
        -------
            The range in the currently selected unit.

            If vehicle is fuel only returns None
            If vehicle doesn't support battery range returns None
        """
        if self._electric:
            return convert_distance(
                self._metric,
                self._electric.ev_range.unit,
                self._electric.ev_range.value,
            )

        return None

    @property
    def battery_range_with_ac(self) -> Optional[float]:
        """The range using _only_ EV when using AC.

        Returns
        -------
            The range in the currently selected unit.

            If vehicle is fuel only returns 0
            If vehicle doesn't support battery range returns 0
        """
        if self._electric:
            return convert_distance(
                self._metric,
                self._electric.ev_range_with_ac.unit,
                self._electric.ev_range_with_ac.value,
            )

        return None

    @property
    def range(self) -> Optional[float]:
        """The range using all available fuel & EV.

        Returns
        -------
            The range in the currently selected unit.

            fuel only == fuel_range
            ev only == battery_range_with_ac
            hybrid == fuel_range + battery_range_with_ac
            None if not supported
        """
        if self._telemetry.distance_to_empty:
            return convert_distance(
                self._metric,
                self._telemetry.distance_to_empty.unit,
                self._telemetry.distance_to_empty.value,
            )

        return None

    @property
    def charging_status(self) -> Optional[str]:
        """Current charging status.

        Returns
        -------
            A string containing the charging status as reported by the vehicle
            None if vehicle doesn't support charging
        """
        return self._electric.charging_status if self._electric else None

    @property
    def remaining_charge_time(self) -> Optional[timedelta]:
        """Time left until charge is complete.

        Returns
        -------
            The amount of time left
            None if vehicle is not currently charging.
            None if vehicle doesn't support charging
        """
        return self._electric.remaining_charge_time if self._electric else None

    @property
    def warning_lights(self) -> Optional[List[Any]]:
        """Dashboard Warning Lights.

        Returns
        -------
            List of latest dashboard warning lights
            _Note_ Not fully understood
        """
        return self._health.warning if self._health else None
