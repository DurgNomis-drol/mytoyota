"""pytest tests for mytoyota using httpx mocking."""
import json

import pytest
from pytest_httpx import HTTPXMock

from mytoyota import MyT


@pytest.mark.asyncio
async def test_authenticate(httpx_mock: HTTPXMock):  # noqa: D103
    with open("./data/mocks/authenticate_working.json") as f:  # noqa: ASYNC101  # I cant see a problem for the tests
        routes = json.load(f)

    for route in routes:
        httpx_mock.add_response(
            method=route["request"]["method"],
            url=route["request"]["url"],
            status_code=route["response"]["status"],
            content=route["response"]["content"],
            headers=route["response"]["headers"],
        )

    client = MyT("user@email.com", "password")
    await client.login()
