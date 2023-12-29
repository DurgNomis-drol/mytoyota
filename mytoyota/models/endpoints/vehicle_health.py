"""Toyota Connected Services API - Endpoint Model."""
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel


class VehicleHealthModel(BaseModel):
    r"""Model representing the health status of a vehicle.

    Attributes
    ----------
        quantity_of_eng_oil_icon (Optional[List[Any]], optional): \n
        The quantity of engine oil icon. Defaults to None.
        vin (str): The VIN (Vehicle Identification Number) of the vehicle.
        warning (Optional[List[Any]]): The warning information. Defaults to None.
        wng_last_upd_time (datetime): The timestamp of the last warning update.

    """

    quantity_of_eng_oil_icon: Optional[List[Any]] = Field(
        alias="quantityOfEngOilIcon"
    )  # TODO unsure what this returns
    vin: str
    warning: Optional[List[Any]]  # TODO unsure what this returns
    wng_last_upd_time: datetime = Field(alias="wnglastUpdTime")


class VehicleHealthResponseModel(StatusModel):
    r"""Model representing a vehicle health response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[VehicleHealthModel], optional): The vehicle health payload. \n
        Defaults to None.

    """

    payload: Optional[VehicleHealthModel] = None
