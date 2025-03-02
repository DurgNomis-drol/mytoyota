"""Model for Climate."""

from datetime import datetime, timedelta
from typing import List, Tuple

from mytoyota.models.endpoints.climate import (
    ACOperations,
    ACParameters,
    ClimateOptions,
    ClimateSettingsModel,
    ClimateStatusModel,
)


class ClimateOptionStatus:
    """Climate option status."""

    def __init__(
        self,
        options: ClimateOptions,
    ):
        """Initialise Class.

        Args:
        ----
            options (ClimateOptions, optional): Contains all additional options for climate

        """
        self._options = options

    def __repr__(self):
        """Representation of the climate option status model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def front_defogger(self) -> bool:
        """The front defogger status.

        Returns
        -------
            bool: The status of front defogger

        """
        return self._options.front_defogger

    @property
    def rear_defogger(self) -> bool:
        """The rear defogger status.

        Returns
        -------
            bool: The status of rear defogger

        """
        return self._options.rear_defogger


class ClimateStatus:
    """Climate status."""

    def __init__(
        self,
        climate_status: ClimateStatusModel,
    ):
        """Initialise Class.

        Args:
        ----
            climate_status (ClimateStatusModel, required): Contains all information
              regarding the climate status

        """
        self._climate_status = climate_status.payload

    def __repr__(self):
        """Representation of the climate status model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def type(self) -> str:
        """The type.

        Returns
        -------
            str: The type

        """
        return self._climate_status.type

    @property
    def status(self) -> bool:
        """The status.

        Returns
        -------
            bool: The status

        """
        return self._climate_status.status

    @property
    def start_time(self) -> datetime | None:
        """Start time.

        Returns
        -------
            datetime: Start time

        """
        return self._climate_status.started_at

    @property
    def duration(self) -> timedelta | None:
        """The duration.

        Returns
        -------
            timedelta: The duration

        """
        if self._climate_status.duration is None:
            return None

        return timedelta(seconds=self._climate_status.duration)

    @property
    def current_temperature(self) -> Tuple[float, str] | None:
        """The current temperature.

        Returns
        -------
            float: The current temperature
            str: The current temperature unit

        """
        if self._climate_status.current_temperature is None:
            return None

        return (
            self._climate_status.current_temperature.value,
            self._climate_status.current_temperature.unit,
        )

    @property
    def target_temperature(self) -> Tuple[float, str] | None:
        """The target temperature.

        Returns
        -------
            float: The target temperature
            str: The target temperature unit

        """
        if self._climate_status.target_temperature is None:
            return None

        return (
            self._climate_status.target_temperature.value,
            self._climate_status.target_temperature.unit,
        )

    @property
    def options(self) -> ClimateOptionStatus | None:
        """The status of climate options.

        Returns
        -------
            ClimateOptionsStatus: The statuses of climate options

        """
        if self._climate_status.options is None:
            return None

        return ClimateOptionStatus(self._climate_status.options)


class ClimateSettingsParameter:
    """Climate settings parameter."""

    def __init__(
        self,
        parameter: ACParameters,
    ):
        """Initialise Class.

        Args:
        ----
            parameter (ACParameters, optional): Contains all parameters

        """
        self._parameter = parameter

    def __repr__(self):
        """Representation of the climate settings parameter model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def available(self) -> bool | None:
        """The parameter avaiability.

        Returns
        -------
            bool | None: The parameter avaiability value

        """
        return self._parameter.available

    @property
    def enabled(self) -> bool:
        """The parameter enable.

        Returns
        -------
            bool: The parameter enable value

        """
        return self._parameter.available

    @property
    def display_name(self) -> str | None:
        """The parameter display name.

        Returns
        -------
            bool: The parameter display name

        """
        return self._parameter.display_name

    @property
    def name(self) -> str:
        """The parameter name.

        Returns
        -------
            bool: The parameter name

        """
        return self._parameter.name

    @property
    def icon_url(self) -> str | None:
        """The parameter icon url.

        Returns
        -------
            bool: The parameter icon url

        """
        return self._parameter.icon_url


class ClimateSettingsOperation:
    """Climate settings operation."""

    def __init__(
        self,
        operation: ACOperations,
    ):
        """Initialise Class.

        Args:
        ----
            operation (ACOperations): Contains all options for climate

        """
        self._operation = operation

    def __repr__(self):
        """Representation of the climate settings operation model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def available(self) -> bool | None:
        """The operation avaiability.

        Returns
        -------
            bool | None: The operation avaiability value

        """
        return self._operation.available

    @property
    def category_name(self) -> str:
        """The operation category name.

        Returns
        -------
            bool: The operation category name

        """
        return self._operation.category_name

    @property
    def category_display_name(self) -> str | None:
        """The operation category display name.

        Returns
        -------
            bool: The operation category display name

        """
        return self._operation.category_display_name

    @property
    def parameters(self) -> List[ClimateSettingsParameter] | None:
        """The operation parameter.

        Returns
        -------
            bool: The operation parameter

        """
        if self._operation.ac_parameters is None:
            return None

        return List[
            (ClimateSettingsParameter(p) for p in self._operation.ac_parameters)
        ]


class ClimateSettings:
    """Climate settings."""

    def __init__(
        self,
        climate_settings: ClimateSettingsModel,
    ):
        """Initialise Class.

        Args:
        ----
            climate_settings (ClimateSettingsModel, required): Contains all information
                regarding the climate settings

        """
        self._climate_settings = climate_settings.payload

    def __repr__(self):
        """Representation of the climate settings model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def settings_on(self) -> bool:
        """The settings on value.

        Returns
        -------
            bool: The value of settings on

        """
        return self._climate_settings.settings_on

    @property
    def temp_interval(self) -> float | None:
        """The temperature interval.

        Returns
        -------
            float | None: The value of temperature interval

        """
        return self._climate_settings.temp_interval

    @property
    def min_temp(self) -> float | None:
        """The min temperature.

        Returns
        -------
            float | None: The value of min temperature

        """
        return self._climate_settings.min_temp

    @property
    def max_temp(self) -> float | None:
        """The max temperature.

        Returns
        -------
            float | None: The value of max temperature

        """
        return self._climate_settings.max_temp

    @property
    def temperature(self) -> tuple[float, str]:
        """The temperature.

        Returns
        -------
            float | None: The value of temperature
            str: The temperature unit

        """
        return (
            self._climate_settings.temperature,
            self._climate_settings.temperature_unit,
        )

    @property
    def operations(self) -> List[ClimateSettingsOperation] | None:
        """The climate operation settings.

        Returns
        -------
            ClimateOperation: The settings of climate operation

        """
        if self._climate_settings.ac_operations is None:
            return None

        return (
            ClimateSettingsOperation(p) for p in self._climate_settings.ac_operations
        )
