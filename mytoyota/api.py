"""Toyota Connected Services API"""
from typing import Optional

from .const import BASE_URL, BASE_URL_CARS
from .controller import Controller


class Api:
    """Controller class."""

    def __init__(self, controller: Controller) -> None:
        """Toyota Controller"""

        self.controller = controller

    async def uuid(self):
        """Returns uuid from controller"""
        return await self.controller.get_uuid()

    async def set_vehicle_alias_endpoint(
        self, new_alias: str, vehicle_id: int
    ) -> Optional[dict]:
        """Set vehicle alias."""

        return await self.controller.request(
            method="PUT",
            base_url=BASE_URL_CARS,
            endpoint=f"/api/users/{await self.uuid()}/vehicles/{vehicle_id}",
            body={"id": vehicle_id, "alias": new_alias},
        )

    async def get_vehicles_endpoint(self) -> Optional[list]:
        """Retrieves list of cars you have registered with MyT"""

        arguments = "?services=uio&legacy=true"

        return await self.controller.request(
            method="GET",
            base_url=BASE_URL_CARS,
            endpoint=f"/vehicle/user/{await self.uuid()}/vehicles{arguments}",
        )

    async def get_connected_services_endpoint(self, vin: str) -> Optional[dict]:
        """Get information about connected services for the given car."""

        arguments = "?legacy=true&services=fud,connected"

        return await self.controller.request(
            method="GET",
            base_url=BASE_URL_CARS,
            endpoint=f"/vehicle/user/{await self.uuid()}/vehicle/{vin}{arguments}",
        )

    async def get_odometer_endpoint(self, vin: str) -> Optional[list]:
        """Get information from odometer."""

        return await self.controller.request(
            method="GET",
            base_url=BASE_URL,
            endpoint=f"/vehicle/{vin}/addtionalInfo",
        )

    async def get_parking_endpoint(self, vin: str) -> Optional[dict]:
        """Get where you have parked your car."""

        return await self.controller.request(
            method="GET",
            base_url=BASE_URL,
            endpoint=f"/users/{await self.uuid()}/vehicle/location",
            headers={"VIN": vin},
        )

    async def get_vehicle_status_endpoint(self, vin: str) -> Optional[dict]:
        """Get information about the vehicle."""

        return await self.controller.request(
            method="GET",
            base_url=BASE_URL,
            endpoint=f"/users/{await self.uuid()}/vehicles/{vin}/vehicleStatus",
        )

    async def get_vehicle_status_legacy_endpoint(self, vin: str) -> Optional[dict]:
        """Get information about the vehicle."""

        return await self.controller.request(
            method="GET",
            base_url=BASE_URL,
            endpoint=f"/vehicles/{vin}/remoteControl/status",
        )

    async def get_driving_statistics_endpoint(
        self, vin: str, from_date: str, interval: Optional[str] = None
    ) -> Optional[dict]:
        """Get driving statistic"""

        return await self.controller.request(
            method="GET",
            base_url=BASE_URL,
            endpoint="/v2/trips/summarize",
            headers={"vin": vin},
            params={"from": from_date, "calendarInterval": interval},
        )
