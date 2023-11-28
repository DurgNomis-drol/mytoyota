""" pytest tests for mytoyota.models.endpoints

    The tests are fairly basic and only test a given JSON is imported by
    pydantic correctly
"""
import pytest
import json

from mytoyota.models.endpoints.account import AccountResponseModel
from mytoyota.models.endpoints.electric import ElectricResponseModel
from mytoyota.models.endpoints.location import LocationResponseModel
from mytoyota.models.endpoints.notifications import NotificationResponse
from mytoyota.models.endpoints.trips import TripsResponseModel
from mytoyota.models.endpoints.vehicle_guid import VehiclesResponseModel
from mytoyota.models.endpoints.vehicle_health import VehicleHealthResponseModel



@pytest.mark.parametrize(
    "model,json_file",
    [
        (AccountResponseModel, "v4accountmodel"),
        (VehiclesResponseModel, "v2vehicleguid"),
        (VehicleHealthResponseModel, "v1_vehicle_health_ok"),
        (VehicleHealthResponseModel, "v1_vehicle_health_error"),
        (LocationResponseModel, "v1_location_ok"),
        (LocationResponseModel, "v1_location_error"),
        (TripsResponseModel, "v1_trips"),
        (ElectricResponseModel, "v1_global_remote_electric_status"),
#        (NotificationResponse, "")
    ],
)
def test_models(model, json_file):
    with open(f"tests/data/endpoints/{json_file}.json", "r") as f:
        json_data = json.load(f)
        model(**json_data)

