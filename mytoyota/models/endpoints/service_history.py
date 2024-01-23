"""Toyota Connected Services API - Service History Models."""

from datetime import date
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel


class ServiceHistoryModel(BaseModel):
    """Represents a service history record.

    Attributes
    ----------
        customer_created_record (bool): Indicates if the record was created by the customer.
        mileage (Optional[int]): The mileage at the time of the service.
        notes (Any): Additional notes about the service.
        operations_performed (Any): The operations performed during the service.
        ro_number (Any): The RO (Repair Order) number associated with the service.
        service_category (str): The category of the service.
        service_date (date): The date of the service.
        service_history_id (str): The ID of the service history record.
        service_provider (str): The service provider.
        servicing_dealer (Any): The dealer that performed the service.
        unit (Optional[str]): The unit associated with the service mileage.

    """

    customer_created_record: bool = Field(alias="customerCreatedRecord")
    mileage: Optional[int] = None
    notes: Any
    operations_performed: Any = Field(alias="operationsPerformed")
    ro_number: Any = Field(alias="roNumber")
    service_category: str = Field(alias="serviceCategory")
    service_date: date = Field(alias="serviceDate")
    service_history_id: str = Field(alias="serviceHistoryId")
    service_provider: str = Field(alias="serviceProvider")
    servicing_dealer: Any = Field(alias="servicingDealer")
    unit: Optional[str] = None


class ServiceHistoriesModel(BaseModel):
    r"""Model representing a list of service histories.

    Attributes
    ----------
        service_histories (List[Optional[ServiceHistoryModel]]): A list of all service histories.
          Defaults to [].

    """

    service_histories: List[Optional[ServiceHistoryModel]] = Field(
        alias="serviceHistories", default=[]
    )


class ServiceHistoryResponseModel(StatusModel):
    """Model representing a service history response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[ServiceHistoriesModel]): The service history payload. Defaults to None.

    """

    payload: Optional[ServiceHistoriesModel] = None
