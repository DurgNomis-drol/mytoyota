"""Toyota Connected Services API - Electric Models."""
from datetime import datetime
from typing import Optional

from pydantic.v1 import Field

from pytoyoda.models.endpoints.common import StatusModel, UnitValueModel
from pytoyoda.utils.models import CustomBaseModel


class ElectricStatusModel(CustomBaseModel):
    r"""Model representing the status of an electric vehicle.

    Attributes
    ----------
        battery_level (int): The battery level of the electric vehicle.
        can_set_next_charging_event Optional[bool]: Indicates whether the next \n
            charging event can be set.
        charging_status (str): The charging status of the electric vehicle.
        ev_range (UnitValueModel): The electric vehicle range.
        ev_range_with_ac (UnitValueModel): The electric vehicle range with AC.
        fuel_level (int): The fuel level of the electric vehicle.
        fuel_range (UnitValueModel): The fuel range of the electric vehicle.
        last_update_timestamp (datetime): The timestamp of the last update.
        remaining_charge_time Optional[int]: The time till full in minutes.

    """

    battery_level: Optional[int] = Field(alias="batteryLevel")
    can_set_next_charging_event: Optional[bool] = Field(
        alias="canSetNextChargingEvent", default=None
    )
    charging_status: Optional[str] = Field(alias="chargingStatus")
    ev_range: Optional[UnitValueModel] = Field(alias="evRange")
    ev_range_with_ac: Optional[UnitValueModel] = Field(alias="evRangeWithAc")
    fuel_level: Optional[int] = Field(alias="fuelLevel", default=None)
    fuel_range: Optional[UnitValueModel] = Field(alias="fuelRange", default=None)
    last_update_timestamp: Optional[datetime] = Field(alias="lastUpdateTimestamp")
    remaining_charge_time: Optional[int] = Field(
        alias="remainingChargeTime",
        default=None,
    )  # TODO: Use field serializer to create timedelta


class ElectricResponseModel(StatusModel):
    r"""Model representing an electric vehicle response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[ElectricStatusModel], optional): The electric vehicle status payload. \n
            Defaults to None.

    """

    payload: Optional[ElectricStatusModel] = None
