"""Toyota Connected Services API - Status Models."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel, UnitValueModel


class _ValueStatusModel(BaseModel):
    value: str
    status: int


class SectionModel(BaseModel):
    """Model representing the status category of a vehicle.

    Attributes
    ----------
        section (str): The section of a vehicle status category.
        values (List[_ValueStatusModel]): A list of values corresponding status informations.

    """

    section: str
    values: List[_ValueStatusModel]


class VehicleStatusModel(BaseModel):
    """Model representing the status category of a vehicle.

    Attributes
    ----------
        category (str): The status category of the vehicle.
        display_order (int): The order in which the status category is displayed
            inside the MyToyota App.
        sections (List[SectionModel]): The different sections belonging to the category.

    """

    category: str
    display_order: int = Field(alias="displayOrder")
    sections: List[SectionModel]


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

    vehicle_status: List[VehicleStatusModel] = Field(alias="vehicleStatus")
    telemetry: _TelemetryModel
    occurrence_date: datetime = Field(alias="occurrenceDate")
    caution_overall_count: int = Field(alias="cautionOverallCount")
    latitude: float
    longitude: float
    location_acquisition_datetime: datetime = Field(alias="locationAcquisitionDatetime")


class RemoteStatusResponseModel(StatusModel):
    r"""Model representing a remote status response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[RemoteStatusModel], optional): The remote status payload. \n
            Defaults to None.

    """

    payload: Optional[RemoteStatusModel] = None
