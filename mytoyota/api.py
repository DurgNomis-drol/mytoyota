"""Toyota Connected Services API"""
from __future__ import annotations

from typing import Any

from .const import BASE_URL, BASE_URL_CARS
from .controller import Controller


class Api:
    """Controller class."""

    def __init__(self, controller: Controller) -> None:
        """Toyota Controller"""
        self.controller = controller

    @property
    def uuid(self) -> str | None:
        """Returns uuid from controller"""
        return self.controller.uuid

    async def set_vehicle_alias_endpoint(
        self, new_alias: str, vehicle_id: int
    ) -> dict[str, Any] | None:
        """Set vehicle alias."""
        return await self.controller.request(
            method="PUT",
            base_url=BASE_URL_CARS,
            endpoint=f"/api/users/{self.uuid}/vehicles/{vehicle_id}",
            body={"id": vehicle_id, "alias": new_alias},
        )

    async def get_vehicles_endpoint(self) -> list[dict[str, Any] | None] | None:
        """Retrieves list of cars you have registered with MyT"""
        return await self.controller.request(
            method="GET",
            base_url=BASE_URL_CARS,
            endpoint=f"/vehicle/user/{self.uuid}/vehicles?services=uio&legacy=true",
        )

    async def get_connected_services_endpoint(self, vin: str) -> dict[str, Any] | None:
        """Get information about connected services for the given car."""
        return await self.controller.request(
            method="GET",
            base_url=BASE_URL_CARS,
            endpoint=f"/vehicle/user/{self.uuid}/vehicle/{vin}?legacy=true&services=fud,connected",
        )

    async def get_odometer_endpoint(self, vin: str) -> list[dict[str, Any]] | None:
        """Get information from odometer."""
        return await self.controller.request(
            method="GET",
            base_url=BASE_URL,
            endpoint=f"/vehicle/{vin}/addtionalInfo",
        )

    async def get_parking_endpoint(self, vin: str) -> dict[str, Any] | None:
        """Get where you have parked your car."""
        return await self.controller.request(
            method="GET",
            base_url=BASE_URL,
            endpoint=f"/users/{self.uuid}/vehicle/location",
            headers={"VIN": vin},
        )

    async def get_vehicle_status_endpoint(self, vin: str) -> dict[str, Any] | None:
        """Get information about the vehicle."""
        return await self.controller.request(
            method="GET",
            base_url=BASE_URL,
            endpoint=f"/users/{self.uuid}/vehicles/{vin}/vehicleStatus",
        )

    async def get_vehicle_status_legacy_endpoint(
        self, vin: str
    ) -> dict[str, Any] | None:
        """Get information about the vehicle."""
        return await self.controller.request(
            method="GET",
            base_url=BASE_URL,
            endpoint=f"/vehicles/{vin}/remoteControl/status",
        )

    async def get_driving_statistics_endpoint(
        self, vin: str, from_date: str, interval: str | None = None
    ) -> dict[str, Any] | None:
        """Get driving statistic"""
        return await self.controller.request(
            method="GET",
            base_url=BASE_URL,
            endpoint="/v2/trips/summarize",
            headers={"vin": vin},
            params={"from": from_date, "calendarInterval": interval},
        )
