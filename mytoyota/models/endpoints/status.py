"""Toyota Connected Services API - Status Models."""
from datetime import datetime
from typing import List, Optional

from pydantic import Field

from mytoyota.models.endpoints.common import StatusModel, UnitValueModel
from mytoyota.utils.models import CustomBaseModel


class _ValueStatusModel(CustomBaseModel):
    value: Optional[str] = None
    status: Optional[int] = None


class SectionModel(CustomBaseModel):
    """Model representing the status category of a vehicle.

    Attributes
    ----------
        section (str): The section of a vehicle status category.
        values (List[_ValueStatusModel]): A list of values corresponding status informations.

    """

    section: Optional[str] = None
    values: Optional[List[_ValueStatusModel]] = None


class VehicleStatusModel(CustomBaseModel):
    """Model representing the status category of a vehicle.

    Attributes
    ----------
        category (str): The status category of the vehicle.
        display_order (int): The order in which the status category is displayed
            inside the MyToyota App.
        sections (List[SectionModel]): The different sections belonging to the category.

    """

    category: Optional[str] = None
    display_order: Optional[int] = Field(None, alias="displayOrder")
    sections: Optional[List[SectionModel]] = None


class _TelemetryModel(CustomBaseModel):
    fugage: Optional[UnitValueModel] = None
    rage: Optional[UnitValueModel] = None
    odo: Optional[UnitValueModel] = None


class RemoteStatusModel(CustomBaseModel):
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

    vehicle_status: Optional[List[VehicleStatusModel]] = Field(None, alias="vehicleStatus")
    telemetry: Optional[_TelemetryModel] = None
    occurrence_date: Optional[datetime] = Field(None, alias="occurrenceDate")
    caution_overall_count: Optional[int] = Field(None, alias="cautionOverallCount")
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_acquisition_datetime: Optional[datetime] = Field(None, alias="locationAcquisitionDatetime")


class RemoteStatusResponseModel(StatusModel):
    r"""Model representing a remote status response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[RemoteStatusModel], optional): The remote status payload. \n
            Defaults to None.

    """

    payload: Optional[RemoteStatusModel] = None
