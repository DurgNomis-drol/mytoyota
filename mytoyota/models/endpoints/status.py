""" Toyota Connected Services API - V1 Status Models """
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel


class _ValueModel(BaseModel):
    value: str
    status: int


class _SectionModel(BaseModel):
    section: str
    values: List[_ValueModel]


class _VehicleStatusModel(BaseModel):
    category: str
    display_order: int = Field(alias="displayOrder")
    sections: List[_SectionModel]


class _FugageModel(BaseModel):
    value: float
    unit: str


class _RageModel(BaseModel):
    value: float
    unit: str


class _OdoModel(BaseModel):
    value: float
    unit: str


class _TelemetryModel(BaseModel):
    fugage: _FugageModel
    rage: _RageModel
    odo: _OdoModel


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
