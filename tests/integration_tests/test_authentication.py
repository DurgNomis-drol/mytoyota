"""pytest tests for mytoyota using httpx mocking."""
import json
from datetime import datetime, timedelta
from pathlib import Path
from shutil import copy2
from typing import List

import pytest
from pytest_httpx import HTTPXMock

from mytoyota import MyT
from mytoyota.controller import CACHE_FILENAME
from mytoyota.exceptions import ToyotaInvalidUsernameError, ToyotaLoginError


def build_routes(httpx_mock: HTTPXMock, filenames: List[str]) -> None:  # noqa: D103
    for filename in filenames:
        # TODO: Move to fixture once I know how to use a fixture from a fixture
        path: str = f"{Path(__file__).parent}/data/"

        with open(
            f"{path}/{filename}", encoding="utf-8"
        ) as f:  # I cant see a problem for the tests
            routes = json.load(f)

        for route in routes:
            httpx_mock.add_response(
                method=route["request"]["method"],
                url=route["request"]["url"],
                status_code=route["response"]["status"],
                content=route["response"]["content"]
                if isinstance(route["response"]["content"], str)
                else json.dumps(route["response"]["content"]),
                headers=route["response"]["headers"],
            )


@pytest.mark.asyncio
@pytest.mark.usefixtures("remove_cache")
async def test_authenticate(httpx_mock):  # noqa: D103
    build_routes(httpx_mock, ["authenticate_working.json"])

    client = MyT("user@email.com", "password")
    # Nothing validates this is correct, just replays a "correct" authentication sequence
    await client.login()


@pytest.mark.asyncio
@pytest.mark.usefixtures("remove_cache")
async def test_authenticate_invalid_username(httpx_mock: HTTPXMock):  # noqa: D103
    build_routes(httpx_mock, ["authenticate_invalid_username.json"])

    client = MyT("user@email.com", "password")
    # Nothing validates this is correct, just replays an invalid username authentication sequence
    with pytest.raises(ToyotaInvalidUsernameError):
        await client.login()


@pytest.mark.asyncio
@pytest.mark.usefixtures("remove_cache")
async def test_authenticate_invalid_password(httpx_mock: HTTPXMock):  # noqa: D103
    build_routes(httpx_mock, ["authenticate_invalid_password.json"])

    client = MyT("user@email.com", "password")
    # Nothing validates this is correct, just replays an invalid username authentication sequence
    with pytest.raises(ToyotaLoginError):
        await client.login()


@pytest.mark.asyncio
async def test_authenticate_refresh_token(data_folder, httpx_mock: HTTPXMock):  # noqa: D103
    # Ensure expired cache file.
    copy2(f"{data_folder}/cached_token.json", CACHE_FILENAME)
    build_routes(httpx_mock, ["authenticate_refresh_token.json"])

    client = MyT("user@email.info", "password")
    # Nothing validates this is correct, just replays a refresh token sequence
    await client.login()


@pytest.mark.asyncio
async def test_get_static_data(data_folder, httpx_mock: HTTPXMock):  # noqa: D103
    #  Create valid token => Means no authentication requests
    with open(f"{data_folder}/cached_token.json", encoding="utf-8") as f:  # noqa: ASYNC101. I dont see this as a problem in test code
        valid_token = json.load(f)
        valid_token["expiration"] = datetime.now() + timedelta(hours=4)

        with open(CACHE_FILENAME, "w", encoding="utf-8") as wf:  # noqa: ASYNC101. I dont see this as a problem in test code
            wf.write(json.dumps(valid_token, indent=4, default=str))

    # Ensure expired cache file.
    build_routes(httpx_mock, ["get_static_data.json"])

    client = MyT("user@email.info", "password")
    # Nothing validates this is correct, just replays a refresh token sequence
    await client.login()
    cars = await client.get_vehicles(metric=True)
    car = cars[0]
    await car.update()

    # Check VIN
    assert car.vin == "12345678912345678"

    # Check alias
    assert car.alias == "RAV4"

    # Check Dashboard
    assert car.dashboard.odometer == 9999.975
    assert car.dashboard.fuel_level == 10
    assert car.dashboard.battery_level == 22
    assert car.dashboard.fuel_range == 112.654
    assert car.dashboard.battery_range == 33.0
    assert car.dashboard.battery_range_with_ac == 30
    assert car.dashboard.range == 100
    assert len(car.dashboard.warning_lights) == 0

    # Check location
    assert car.location.latitude == 50.0
    assert car.location.longitude == 0.0

    # Check Notifications
    assert len(car.notifications) == 3
    assert (
        car.notifications[0].message
        == "2020 RAV4 PHEV: Climate control was interrupted (Door open) [1]"
    )
    assert car.notifications[0].type == "alert"
    assert car.notifications[0].category == "RemoteCommand"
    assert (
        car.notifications[1].message
        == "2020 RAV4 PHEV: Climate was started and will automatically shut off."
    )
    assert car.notifications[2].message == "2020 RAV4 PHEV: Charging Interrupted [4]."
