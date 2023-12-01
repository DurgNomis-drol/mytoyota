"""Toyota Connected Services API - Status Models."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel, UnitValueModel


class _ValueStatusModel(BaseModel):
    value: str
    status: int


class _SectionModel(BaseModel):
    section: str
    values: List[_ValueStatusModel]


class _VehicleStatusModel(BaseModel):
    category: str
    display_order: int = Field(alias="displayOrder")
    sections: List[_SectionModel]


class _TelemetryModel(BaseModel):
    fugage: UnitValueModel
    rage: UnitValueModel
    odo: UnitValueModel


class RemoteStatusModel(BaseModel):
    """Model representing the remote status of a vehicle.

    Attributes
    ----------
        vehicle_status (List[_VehicleStatusModel]): The status of the vehicle.
        telemetry (_TelemetryModel): The telemetry data of the vehicle.
        occurrence_date (datetime): The date of the occurrence.
        caution_overall_count (int): The overall count of cautions.
        latitude (float): The latitude of the vehicle's location.
        longitude (float): The longitude of the vehicle's location.
        location_acquisition_datetime (datetime): The datetime of location acquisition.

    """

    vehicle_status: List[_VehicleStatusModel] = Field(alias="vehicleStatus")
    telemetry: _TelemetryModel
    occurrence_date: datetime = Field(alias="occurrenceDate")
    caution_overall_count: int = Field(alias="cautionOverallCount")
    latitude: float
    longitude: float
    location_acquisition_datetime: datetime = Field(alias="locationAcquisitionDatetime")


class RemoteStatusResponseModel(StatusModel):
    """Model representing a remote status response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[RemoteStatusModel], optional): The remote status payload. Defaults to None.

    """

    payload: Optional[RemoteStatusModel] = None
