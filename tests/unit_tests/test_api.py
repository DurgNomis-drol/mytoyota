"""pytest tests for pytoyoda.api."""
import json
from datetime import date, timedelta
from unittest.mock import AsyncMock

import pytest

from pytoyoda.api import Api
from pytoyoda.const import (
    VEHICLE_GLOBAL_REMOTE_ELECTRIC_STATUS_ENDPOINT,
    VEHICLE_GLOBAL_REMOTE_STATUS_ENDPOINT,
    VEHICLE_GUID_ENDPOINT,
    VEHICLE_HEALTH_STATUS_ENDPOINT,
    VEHICLE_LOCATION_ENDPOINT,
    VEHICLE_NOTIFICATION_HISTORY_ENDPOINT,
    VEHICLE_SERVICE_HISTORY_ENDPONT,
    VEHICLE_TELEMETRY_ENDPOINT,
    VEHICLE_TRIPS_ENDPOINT,
)
from pytoyoda.models.endpoints.electric import ElectricResponseModel
from pytoyoda.models.endpoints.location import LocationResponseModel
from pytoyoda.models.endpoints.notifications import NotificationResponseModel
from pytoyoda.models.endpoints.service_history import ServiceHistoryResponseModel

# from pytoyoda.models.endpoints.account import AccountResponseModel
from pytoyoda.models.endpoints.status import RemoteStatusResponseModel
from pytoyoda.models.endpoints.telemetry import TelemetryResponseModel
from pytoyoda.models.endpoints.trips import TripsResponseModel
from pytoyoda.models.endpoints.vehicle_guid import VehiclesResponseModel
from pytoyoda.models.endpoints.vehicle_health import VehicleHealthResponseModel

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
        (
            "GET",
            VEHICLE_GUID_ENDPOINT,
            VehiclesResponseModel,
            "v2_vehicleguid",
            "vehicles-happy",
        ),
        (
            "GET",
            VEHICLE_LOCATION_ENDPOINT,
            LocationResponseModel,
            "v1_location_ok",
            "location-happy",
        ),
        (
            "GET",
            VEHICLE_HEALTH_STATUS_ENDPOINT,
            VehicleHealthResponseModel,
            "v1_vehicle_health_ok",
            "health-happy",
        ),
        (
            "GET",
            VEHICLE_GLOBAL_REMOTE_STATUS_ENDPOINT,
            RemoteStatusResponseModel,
            "v1_global_remote_status",
            "remote-status-happy",
        ),
        (
            "GET",
            VEHICLE_GLOBAL_REMOTE_ELECTRIC_STATUS_ENDPOINT,
            ElectricResponseModel,
            "v1_global_remote_electric_status",
            "electric-status-happy",
        ),
        (
            "GET",
            VEHICLE_TELEMETRY_ENDPOINT,
            TelemetryResponseModel,
            "v3_telemetry",
            "telemetry-happy",
        ),
        (
            "GET",
            VEHICLE_NOTIFICATION_HISTORY_ENDPOINT,
            NotificationResponseModel,
            "v2_notification",
            "notification-happy",
        ),
        (
            "GET",
            VEHICLE_SERVICE_HISTORY_ENDPONT,
            ServiceHistoryResponseModel,
            "v1_service_history",
            "service_history-happy",
        ),
        (
            "GET",
            VEHICLE_TRIPS_ENDPOINT.format(
                from_date=YESTERDAY,
                to_date=TODAY,
                route=False,
                summary=False,
                limit=5,
                offset=0,
            ),
            TripsResponseModel,
            "v1_trips",
            "trips-happy",
        ),
        # Edge cases
        # Add edge cases here
        # Error cases
        (
            "GET",
            VEHICLE_LOCATION_ENDPOINT,
            LocationResponseModel,
            "v1_location_error",
            "location-error",
        ),
        (
            "GET",
            VEHICLE_HEALTH_STATUS_ENDPOINT,
            VehicleHealthResponseModel,
            "v1_vehicle_health_error",
            "health-error",
        ),
    ],
)
async def test_api_request_and_parse_endpoints(  # NOQA: PLR0913
    data_folder, method, endpoint, model, response_data_json_path, test_id
):
    """Test the API for various endpoints.

    Args:
    ----
        data_folder: Path to find data files
        method: The method with which the API endpoint is to be addressed.
        endpoint: The API endpoint to be tested.
        model: The pydantic model class to test.
        response_data_json_path: Path to the JSON file containing the test data.
        test_id: The ID under which the test is displayed in pytest.

    Returns:
    -------
        None

    """
    # Arrange

    with open(  # noqa : ASYNC101
        f"{data_folder}/{response_data_json_path}.json", "r", encoding="utf-8"
    ) as f:
        response_data = json.load(f)

    controller = AsyncMock()
    controller.request_json.return_value = response_data
    api = Api(controller)

    # Act
    response = await api._request_and_parse(model, method, endpoint, vin=VIN)

    # Assert
    controller.request_json.assert_called_once_with(method=method, endpoint=endpoint, vin=VIN)
    assert response == model(**response_data), f"Test ID: {test_id}"
