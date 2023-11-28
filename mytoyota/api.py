"""Toyota Connected Services API"""

from datetime import date, datetime, timezone
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from mytoyota.models.endpoints.location import LocationResponseModel
from mytoyota.models.endpoints.notifications import NotificationResponse
from mytoyota.models.endpoints.status import RemoteStatusResponseModel
from mytoyota.models.endpoints.trips import TripsResponseModel
from mytoyota.models.endpoints.vehicle_guid import VehiclesResponseModel
from mytoyota.models.endpoints.vehicle_health import VehicleHealthResponseModel

from .const import BASE_URL
from .controller import Controller
from .exceptions import ToyotaApiError


class Api:
    """Controller class."""

    def __init__(self, controller: Controller) -> None:
        """Toyota Controller"""
        self.controller = controller

    @property
    def uuid(self) -> Optional[str]:
        """Returns uuid from controller"""
        return self.controller.uuid

    async def set_vehicle_alias_endpoint(self, alias: str, guid: str, vin: str):
        """Set the alias for a vehicle."""
        return await self.controller.request(
            method="PUT",
            base_url=BASE_URL,
            endpoint="/v1/vehicle-association/vehicle",
            headers={
                "datetime": str(int(datetime.now(timezone.utc).timestamp() * 1000)),
                "x-correlationid": str(uuid4()),
                "Content-Type": "application/json",
                "vin": vin,
            },
            body={"guid": guid, "vin": vin, "nickName": alias},
        )

    # TODO What does this do?
    async def get_wake_endpoint(self) -> None:
        """Send a wake request to the vehicle."""
        await self.controller.request(
            method="POST", base_url=BASE_URL, endpoint="/v2/global/remote/wake"
        )

    async def get_vehicles_endpoint(self) -> VehiclesResponseModel:
        """Retrieves list of cars you have registered with MyT"""
        response = await self.controller.request_json(
            method="GET",
            base_url=BASE_URL,
            endpoint="/v2/vehicle/guid",
        )

        return VehiclesResponseModel(**response)

    async def get_location_endpoint(self, vin: str) -> LocationResponseModel:
        """Get where you have parked your car."""
        response = await self.controller.request_json(
            method="GET",
            base_url=BASE_URL,
            endpoint="/v1/location",
            headers={"VIN": vin},
        )

        return LocationResponseModel(**response)

    async def get_vehicle_health_status_endpoint(
        self, vin: str
    ) -> VehicleHealthResponseModel:
        """Get information about the vehicle."""
        response = await self.controller.request_json(
            method="GET",
            base_url=BASE_URL,
            endpoint="/v1/vehiclehealth/status",
            headers={"VIN": vin},
        )

        return VehicleHealthResponseModel(**response)

    async def get_vehicle_status_endpoint(self, vin: str) -> RemoteStatusResponseModel:
        """Get information about the vehicle."""
        response = await self.controller.request_json(
            method="GET",
            base_url=BASE_URL,
            endpoint="/v1/global/remote/status",
            headers={"VIN": vin},
        )

        return RemoteStatusResponseModel(**response)

    async def get_vehicle_electric_status_endpoint(
        self, vin: str
    ) -> Optional[Union[Dict[str, Any], List[Any]]]:
        """Get information about the vehicle."""
        try:
            return await self.controller.request(
                method="GET",
                base_url=BASE_URL,
                endpoint="/v1/global/remote/electric/status",
                headers={"VIN": vin},
            )
        except ToyotaApiError:
            # TODO This is wrong, but lets change the Vehicle class
            return None

    async def get_telemetry_endpoint(
        self, vin: str
    ) -> Optional[Union[Dict[str, Any], List[Any]]]:
        """Get information about the vehicle."""
        return await self.controller.request(
            method="GET",
            base_url=BASE_URL,
            endpoint="/v3/telemetry",
            headers={"vin": vin},
        )

    async def get_notification_endpoint(self, vin: str) -> NotificationResponse:
        """Get information about the vehicle."""
        response = await self.controller.request_json(
            method="GET",
            base_url=BASE_URL,
            endpoint="/v2/notification/history",
            headers={"vin": vin},
        )

        return NotificationResponse(**response)

    async def get_driving_statistics_endpoint(
        self, vin: str, from_date: str, interval: Optional[str] = None
    ) -> Optional[Union[Dict[str, Any], List[Any]]]:
        """Get driving statistic"""
        return await self.controller.request(
            method="GET",
            base_url=BASE_URL,
            endpoint="/v2/trips/summarize",
            headers={"vin": vin},
            params={"from": from_date, "calendarInterval": interval},
        )

    async def get_trips_endpoint(
        self,
        vin: str,
        from_date: date,
        to_date: date,
        route: bool = False,
        summary: bool = True,
        limit: int = 5,
        offset: int = 0,
    ) -> TripsResponseModel:
        """Get trip
        The page parameter works a bit strange but setting to 1 gets last few trips"""
        response = await self.controller.request_json(
            method="GET",
            base_url=BASE_URL,
            endpoint=f"/v1/trips?from={from_date}&to={to_date}&route={route}&summary={summary}&limit={limit}&offset={offset}",  # pylint: disable=C0301
            headers={"vin": vin},
        )

        return TripsResponseModel(**response)
