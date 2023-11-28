""" Toyota Connected Services API - V1 Status Models """
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
    vehicle_status: List[_VehicleStatusModel] = Field(alias="vehicleStatus")
    telemetry: _TelemetryModel
    occurrence_date: datetime = Field(alias="occurrenceDate")
    caution_overall_count: int = Field(alias="cautionOverallCount")
    latitude: float
    longitude: float
    location_acquisition_datetime: datetime = Field(alias="locationAcquisitionDatetime")


class RemoteStatusResponseModel(StatusModel):
    payload: Optional[RemoteStatusModel] = None
