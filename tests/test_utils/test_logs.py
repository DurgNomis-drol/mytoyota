"""Test Logs Utils."""
import pytest
from httpx import Request, Response

from mytoyota.utils.logging.log_utils import (
    censor_all,
    censor_string,
    censor_value,
    format_httpx_response,
)


# Test censor_value function
@pytest.mark.parametrize(
    "value, key, to_censor, expected",
    [
        pytest.param(
            "SensitiveData",
            "authorization",
            {"authorization"},
            "Se***********",
        ),
        pytest.param(123.456, "latitude", {"latitude"}, 123),
        pytest.param(
            {"key1": "value1", "password": "12345"},
            "password",
            {"password"},
            {"key1": "value1", "password": "12***"},
        ),
        pytest.param(
            ["SensitiveData1", "SensitiveData2"],
            "emails",
            {"emails"},
            ["Se************", "Se************"],
        ),
        pytest.param("", "empty", {"empty"}, ""),
        pytest.param("AB", "short", {"short"}, "AB"),
        pytest.param({"key": "value"}, "key", set(), {"key": "value"}),
        pytest.param(None, "none", {"none"}, None),
        pytest.param(123, "int", {"int"}, 123),
    ],
)
def test_censor_value(value, key, to_censor, expected):  # noqa : D103
    # Act
    result = censor_value(value, key, to_censor)

    # Assert
    assert result == expected


# Test censor_all function
@pytest.mark.parametrize(
    "dictionary, to_censor, expected",
    [
        pytest.param(
            {"username": "user123", "password": "secret"},
            {"password"},
            {"username": "user123", "password": "se****"},
        ),
        pytest.param(
            {"latitude": 123.456, "longitude": -123.456},
            {"latitude", "longitude"},
            {"latitude": 123, "longitude": -123},
        ),
        pytest.param(
            {"key": "value"},
            set(),
            {"key": "value"},
        ),
        pytest.param(
            {"username": "user123", "password": None},
            {"password"},
            {"username": "user123", "password": None},
        ),
    ],
)
def test_censor_all(dictionary, to_censor, expected):  # noqa : D103
    # Act
    result = censor_all(dictionary, to_censor)

    # Assert
    assert result == expected


# Test censor_string function
@pytest.mark.parametrize(
    "string, expected",
    [
        pytest.param("SensitiveData", "Se***********"),
        pytest.param("", ""),
        pytest.param("AB", "AB"),
        pytest.param("A", "A"),
    ],
)
def test_censor_string(string, expected):  # noqa: D103
    # Act
    result = censor_string(string)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "method, url, request_headers, request_body, status_code, response_headers, response_body, expected_output",  # noqa : E501
    [
        # Happy path tests
        pytest.param(
            "GET",
            "https://example.com/notfound",
            {"Accept": "application/json"},
            "",
            404,
            {"Content-Type": "text/html"},
            "<html>Not Found</html>",
            "Request:\n  Method : GET\n  URL    : https://example.com/notfound\n  Headers: Headers({'host': 'example.com', 'accept': 'application/json'})\n  Body   : \nResponse:\n  Status : (404,Not Found)\n  Headers: Headers({'content-type': 'text/html', 'content-length': '22'})\n  Content: <html>Not Found</html>",  # noqa : E501
        ),
    ],
)
def test_format_httpx_response(  # noqa : PLR0913
    method,
    url,
    request_headers,
    request_body,
    status_code,
    response_headers,
    response_body,
    expected_output,
):
    # Arrange
    request = Request(
        method=method,
        url=url,
        headers=request_headers,
        content=request_body.encode("utf-8"),
    )
    response = Response(
        status_code=status_code,
        request=request,
        headers=response_headers,
        content=response_body.encode("utf-8"),
    )

    # Act
    output = format_httpx_response(response)

    # Assert
    assert output == expected_output
