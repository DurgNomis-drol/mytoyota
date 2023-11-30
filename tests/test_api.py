"""pytest tests for mytoyota.api"""
import json
from datetime import date, timedelta
from unittest.mock import AsyncMock

import pytest

from mytoyota.api import Api
from mytoyota.models.endpoints.electric import ElectricResponseModel
from mytoyota.models.endpoints.location import LocationResponseModel
from mytoyota.models.endpoints.notifications import NotificationResponseModel

# from mytoyota.models.endpoints.account import AccountResponseModel
from mytoyota.models.endpoints.status import RemoteStatusResponseModel
from mytoyota.models.endpoints.telemetry import TelemetryResponseModel
from mytoyota.models.endpoints.trips import TripsResponseModel
from mytoyota.models.endpoints.vehicle_guid import VehiclesResponseModel
from mytoyota.models.endpoints.vehicle_health import VehicleHealthResponseModel

# Constants for tests
VIN = "Random0815"
GUID = "123e4567-e89b-12d3-a456-426614174000"
ALIAS = "MyCar"
TODAY = date.today()
YESTERDAY = TODAY - timedelta(days=1)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method, endpoint, model, response_data_json_path, test_id",
    [
        # Happy path tests
        ("GET", "/v2/vehicle/guid", VehiclesResponseModel, "v2_vehicleguid", "vehicles-happy"),
        ("GET", "/v1/location", LocationResponseModel, "v1_location_ok", "location-happy"),
        ("GET", "/v1/vehiclehealth/status", VehicleHealthResponseModel, "v1_vehicle_health_ok", "health-happy"),
        (
            "GET",
            "/v1/global/remote/status",
            RemoteStatusResponseModel,
            "v1_global_remote_status",
            "remote-status-happy",
        ),
        (
            "GET",
            "/v1/global/remote/electric/status",
            ElectricResponseModel,
            "v1_global_remote_electric_status",
            "electric-status-happy",
        ),
        ("GET", "/v3/telemetry", TelemetryResponseModel, "v3_telemetry", "telemetry-happy"),
        ("GET", "/v2/notification/history", NotificationResponseModel, "v2_notification", "notification-happy"),
        (
            "GET",
            f"/v1/trips?from={YESTERDAY}&to={TODAY}&route=False&summary=False&limit=5&offset=0",
            TripsResponseModel,
            "v1_trips",
            "trips-happy",
        ),
        # Edge cases
        # Add edge cases here
        # Error cases
        ("GET", "/v1/location", LocationResponseModel, "v1_location_error", "location-error"),
        ("GET", "/v1/vehiclehealth/status", VehicleHealthResponseModel, "v1_vehicle_health_error", "health-error"),
    ],
)
async def test_api_request_and_parse_endpoints(method, endpoint, model, response_data_json_path, test_id):
    """
    Test the API for various endpoints.

    Args:
        model: The model class to test.
        response_data_json_path: Path to the JSON file containing the test data.

    Returns:
        None

    """
    # Arrange

    with open(f"tests/data/endpoints/{response_data_json_path}.json", "r", encoding="utf-8") as f:
        response_data = json.load(f)

    controller = AsyncMock()
    controller.request_json.return_value = response_data
    api = Api(controller)

    # Act
    response = await api._request_and_parse(model, method, endpoint, vin=VIN)  # pylint: disable=W0212

    # Assert
    controller.request_json.assert_called_once_with(method=method, endpoint=endpoint, vin=VIN)
    assert response == model(**response_data), f"Test ID: {test_id}"
