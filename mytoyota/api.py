"""Toyota Connected Services API"""

from datetime import date, datetime, timezone
from uuid import uuid4

from mytoyota.models.endpoints.electric import ElectricResponseModel
from mytoyota.models.endpoints.location import LocationResponseModel
from mytoyota.models.endpoints.notifications import NotificationResponseModel
from mytoyota.models.endpoints.status import RemoteStatusResponseModel
from mytoyota.models.endpoints.telemetry import TelemetryResponseModel
from mytoyota.models.endpoints.trips import TripsResponseModel
from mytoyota.models.endpoints.vehicle_guid import VehiclesResponseModel
from mytoyota.models.endpoints.vehicle_health import VehicleHealthResponseModel

from .controller import Controller


class Api:
    """Controller class."""

    def __init__(self, controller: Controller) -> None:
        """Toyota Controller"""
        self.controller = controller

    async def _request_and_parse(self, model, method: str, endpoint: str, **kwargs):
        """Generic request and response parsing."""
        response = await self.controller.request_json(
            method=method, endpoint=endpoint, **kwargs
        )
        return model(**response)

    async def set_vehicle_alias_endpoint(self, alias: str, guid: str, vin: str):
        """Set the alias for a vehicle."""
        return await self.controller.request(
            method="PUT",
            endpoint="/v1/vehicle-association/vehicle",
            vin=vin,
            headers={
                "datetime": str(int(datetime.now(timezone.utc).timestamp() * 1000)),
                "x-correlationid": str(uuid4()),
                "Content-Type": "application/json",
            },
            body={"guid": guid, "vin": vin, "nickName": alias},
        )

    #    TODO: Remove for now as it seems to have no effect. The App is sending it!
    #    async def post_wake_endpoint(self) -> None:
    #        """Send a wake request to the vehicle."""
    #        await self.controller.request_raw(
    #            method="POST", endpoint="/v2/global/remote/wake"
    #        )

    async def get_vehicles_endpoint(self) -> VehiclesResponseModel:
        """Retrieves list of vehicles registered with provider"""
        endpoint = "/v2/vehicle/guid"
        return await self._request_and_parse(VehiclesResponseModel, "GET", endpoint)

    async def get_location_endpoint(self, vin: str) -> LocationResponseModel:
        """Get where you have parked your car."""
        endpoint = "/v1/location"
        return await self._request_and_parse(
            LocationResponseModel, "GET", endpoint, vin=vin
        )

    async def get_vehicle_health_status_endpoint(
        self, vin: str
    ) -> VehicleHealthResponseModel:
        """Get information about the vehicle."""
        endpoint = "/v1/vehiclehealth/status"
        return await self._request_and_parse(
            VehicleHealthResponseModel, "GET", endpoint, vin=vin
        )

    async def get_remote_status_endpoint(self, vin: str) -> RemoteStatusResponseModel:
        """Get information about the vehicle."""
        endpoint = "/v1/global/remote/status"
        return await self._request_and_parse(
            RemoteStatusResponseModel, "GET", endpoint, vin=vin
        )

    async def get_vehicle_electric_status_endpoint(
        self, vin: str
    ) -> ElectricResponseModel:
        """Get information about the vehicle."""
        endpoint = "/v1/global/remote/electric/status"
        return await self._request_and_parse(
            ElectricResponseModel, "GET", endpoint, vin=vin
        )

    async def get_telemetry_endpoint(self, vin: str) -> TelemetryResponseModel:
        """Get information about the vehicle."""
        endpoint = "/v3/telemetry"
        return await self._request_and_parse(
            TelemetryResponseModel, "GET", endpoint, vin=vin
        )

    async def get_notification_endpoint(self, vin: str) -> NotificationResponseModel:
        """Get information about the vehicle."""
        endpoint = "/v2/notification/history"
        return await self._request_and_parse(
            NotificationResponseModel, "GET", endpoint, vin=vin
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
        endpoint = f"/v1/trips?from={from_date}&to={to_date}&route={route}&summary={summary}&limit={limit}&offset={offset}"  # pylint: disable=C0301
        return await self._request_and_parse(
            TripsResponseModel, "GET", endpoint, vin=vin
        )
