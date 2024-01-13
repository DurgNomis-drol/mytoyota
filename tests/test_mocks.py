"""pytest tests for mytoyota using httpx mocking."""
import json
from os import remove
from shutil import copy2
from typing import List

import pytest
from pytest_httpx import HTTPXMock

from mytoyota import MyT
from mytoyota.controller import CACHE_FILENAME
from mytoyota.exceptions import ToyotaInvalidUsernameError, ToyotaLoginError


def remove_cache() -> None:  # noqa: D103
    # Remove cache file if exists
    try:
        remove(CACHE_FILENAME)
    except FileNotFoundError:
        pass


def build_routes(httpx_mock, filenames: List[str]) -> None:  # noqa: D103
    for filename in filenames:
        with open(filename) as f:  # I cant see a problem for the tests
            routes = json.load(f)

        for route in routes:
            httpx_mock.add_response(
                method=route["request"]["method"],
                url=route["request"]["url"],
                status_code=route["response"]["status"],
                content=route["response"]["content"],
                headers=route["response"]["headers"],
            )


@pytest.mark.asyncio
async def test_authenticate(httpx_mock: HTTPXMock):  # noqa: D103
    remove_cache()
    build_routes(httpx_mock, ["./data/mocks/authenticate_working.json"])

    client = MyT("user@email.com", "password")
    # Nothing validates this is correct, just replays a "correct" authentication sequence
    await client.login()


@pytest.mark.asyncio
async def test_authenticate_invalid_username(httpx_mock: HTTPXMock):  # noqa: D103
    remove_cache()
    build_routes(httpx_mock, ["./data/mocks/authenticate_invalid_username.json"])

    client = MyT("user@email.com", "password")
    # Nothing validates this is correct, just replays an invalid username authentication sequence
    with pytest.raises(ToyotaInvalidUsernameError):
        await client.login()


@pytest.mark.asyncio
async def test_authenticate_invalid_password(httpx_mock: HTTPXMock):  # noqa: D103
    remove_cache()
    build_routes(httpx_mock, ["./data/mocks/authenticate_invalid_password.json"])

    client = MyT("user@email.com", "password")
    # Nothing validates this is correct, just replays an invalid username authentication sequence
    with pytest.raises(ToyotaLoginError):
        await client.login()


@pytest.mark.asyncio
async def test_authenticate_refresh_token(httpx_mock: HTTPXMock):  # noqa: D103
    # Ensure expired cache file.
    copy2("./data/mocks/cached_token.json", CACHE_FILENAME)
    build_routes(httpx_mock, ["./data/mocks/authenticate_refresh_token.json"])

    client = MyT("user@email.info", "password")
    # Nothing validates this is correct, just replays a refresh token sequence
    await client.login()
