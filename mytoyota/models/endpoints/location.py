"""Toyota Connected Services API - Location Models."""
from datetime import datetime
from typing import Optional

from pydantic.v1 import Field

from mytoyota.models.endpoints.common import StatusModel
from mytoyota.utils.models import CustomBaseModel


class _VehicleLocationModel(CustomBaseModel):
    display_name: Optional[str] = Field(alias="displayName")
    latitude: Optional[float]
    location_acquisition_datetime: Optional[datetime] = Field(alias="locationAcquisitionDatetime")
    longitude: Optional[float]


class LocationModel(CustomBaseModel):
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
