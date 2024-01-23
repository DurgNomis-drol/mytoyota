"""models for vehicle service history."""
from datetime import date
from typing import Any, Optional

from mytoyota.models.endpoints.service_history import ServiceHistoryModel
from mytoyota.utils.conversions import convert_distance


class ServiceHistory:
    """ServiceHistory."""

    def __init__(
        self,
        service_history: ServiceHistoryModel,
        metric: bool = True,
    ):
        """Initialise ServiceHistory."""
        self._service_history = service_history
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
    def service_date(self) -> date:
        """The date of the service.

        Returns
        -------
            date: The date of the service.
        """
        return self._service_history.service_date

    @property
    def customer_created_record(self) -> bool:
        """Indication whether it is an entry created by the user.

        Returns
        -------
            str: Category of notification
        """
        return self._service_history.customer_created_record

    @property
    def odometer(self) -> Optional[float]:
        """Odometer distance at the time of servicing.

        Returns
        -------
            int: Odometer distance at the time of servicing
                in the current selected units

        """
        if (
            self._service_history is not None
            and self._service_history.unit is not None
            and self._service_history.mileage is not None
        ):
            return convert_distance(
                self._distance_unit,
                self._service_history.unit,
                self._service_history.mileage,
            )
        else:
            return None

    @property
    def notes(self) -> Any:
        """Additional notes about the service.

        Returns
        -------
            Any: Additional notes about the service
        """
        return self._service_history.notes

    @property
    def operations_performed(self) -> Any:
        """The operations performed during the service.

        Returns
        -------
            Any: The operations performed during the service
        """
        return self._service_history.operations_performed

    @property
    def ro_number(self) -> Any:
        """The RO (Repair Order) number associated with the service.

        Returns
        -------
            Any: The RO (Repair Order) number associated with the service
        """
        return self._service_history.ro_number

    @property
    def service_category(self) -> str:
        """The category of the service.

        Returns
        -------
            str: The category of the service.
        """
        return self._service_history.service_category

    @property
    def service_provider(self) -> str:
        """The service provider.

        Returns
        -------
            str: The service provider
        """
        return self._service_history.service_provider

    @property
    def servicing_dealer(self) -> Any:
        """Dealer that performed the service.

        Returns
        -------
            Any: The dealer that performed the service
        """
        return self._service_history.servicing_dealer
