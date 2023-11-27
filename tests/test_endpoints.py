""" pytest tests for mytoyota.models.endpoints

    The tests are fairly basic and only test a given JSON is imported by
    pydantic correctly
"""
import pytest
import json

from mytoyota.models.endpoints.v4_account import V4AccountModel
from mytoyota.models.endpoints.v2_vehicle_guid import VehiclesModel
from mytoyota.models.endpoints.v1_vehicle_health import V1VehicleHealthModel
from mytoyota.models.endpoints.v1_location import V1LocationModel
from mytoyota.models.endpoints.v1_trips import V1TripsModel



@pytest.mark.parametrize(
    "model,json_file",
    [
        (V4AccountModel, "v4accountmodel"),
        (VehiclesModel, "v2vehicleguid"),
        (V1VehicleHealthModel, "v1_vehicle_health_ok"),
        (V1VehicleHealthModel, "v1_vehicle_health_error"),
        (V1LocationModel, "v1_location_ok"),
        (V1LocationModel, "v1_location_error"),
        (V1TripsModel, "v1_trips"),
    ],
)
def test_models(model, json_file):
    with open(f"tests/data/endpoints/{json_file}.json", "r") as f:
        json_data = json.load(f)
        model(**json_data)

