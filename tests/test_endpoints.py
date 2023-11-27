""" pytest tests for mytoyota.models.endpoints

    The tests are fairly basic and only test a given JSON is imported by
    pydantic correctly
"""
import pytest
import json

from mytoyota.models.endpoints.v4_account import V4AccountModel


@pytest.mark.parametrize(
    "model,json_file",
    [
        (V4AccountModel, "v4accountmodel"),
    ],
)
def test_models(model, json_file):
    with open(f"tests/data/endpoints/{json_file}.json", "r") as f:
        json_data = json.load(f)
        model(**json_data)


