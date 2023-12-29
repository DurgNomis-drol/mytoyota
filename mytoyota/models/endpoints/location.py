"""Toyota Connected Services API - Location Models."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from mytoyota.models.endpoints.common import StatusModel


class _VehicleLocationModel(BaseModel):
    display_name: str = Field(alias="displayName")
    latitude: float
    location_acquisition_datetime: datetime = Field(alias="locationAcquisitionDatetime")
    longitude: float


class LocationModel(BaseModel):
    r"""Model representing the location of a vehicle.

    Attributes
    ----------
        last_timestamp (Optional[datetime], optional): The last timestamp of the location. \n
            Defaults to None.
        vehicle_location (Optional[_VehicleLocationModel], optional): The location of
            the vehicle. \n Defaults to None.
        vin (Optional[str], optional): The VIN (Vehicle Identification Number) of the vehicle. \n
            Defaults to None.

    """

    last_timestamp: Optional[datetime] = Field(alias="lastTimestamp", default=None)
    vehicle_location: Optional[_VehicleLocationModel] = Field(
        alias="vehicleLocation", default=None
    )
    vin: Optional[str] = None


class LocationResponseModel(StatusModel):
    """Model representing a location response.

    Inherits from StatusModel.

    Attributes
    ----------
        payload (Optional[LocationModel], optional): The location payload. Defaults to None.

    """

    payload: Optional[LocationModel] = None
