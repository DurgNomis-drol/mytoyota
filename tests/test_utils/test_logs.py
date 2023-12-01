"""Test Logs Utils."""
import pytest

from mytoyota.utils.logs import censor_all, censor_string, censor_value


# Test censor_value function
@pytest.mark.parametrize(
    "test_id, value, key, to_censor, expected",
    [
        ("happy-1", "SensitiveData", "authorization", {"authorization"}, "Se***********"),
        ("happy-2", 123.456, "latitude", {"latitude"}, 123),
        (
            "happy-3",
            {"key1": "value1", "password": "12345"},
            "password",
            {"password"},
            {"key1": "value1", "password": "12***"},
        ),
        ("happy-4", ["SensitiveData1", "SensitiveData2"], "emails", {"emails"}, ["Se************", "Se************"]),
        ("edge-1", "", "empty", {"empty"}, ""),
        ("edge-2", "AB", "short", {"short"}, "AB"),
        ("edge-3", {"key": "value"}, "key", set(), {"key": "value"}),
        ("error-1", None, "none", {"none"}, None),
        ("error-2", 123, "int", {"int"}, 123),
    ],
)
def test_censor_value(test_id, value, key, to_censor, expected):  # noqa: D103, ARG001
    # Act
    result = censor_value(value, key, to_censor)

    # Assert
    assert result == expected


# Test censor_all function
@pytest.mark.parametrize(
    "test_id, dictionary, to_censor, expected",
    [
        (
            "happy-1",
            {"username": "user123", "password": "secret"},
            {"password"},
            {"username": "user123", "password": "se****"},
        ),
        (
            "happy-2",
            {"latitude": 123.456, "longitude": -123.456},
            {"latitude", "longitude"},
            {"latitude": 123, "longitude": -123},
        ),
        (
            "edge-1",
            {"key": "value"},
            set(),
            {"key": "value"},
        ),
        (
            "error-1",
            {"username": "user123", "password": None},
            {"password"},
            {"username": "user123", "password": None},
        ),
    ],
)
def test_censor_all(test_id, dictionary, to_censor, expected):  # noqa: D103, ARG001
    # Act
    result = censor_all(dictionary, to_censor)

    # Assert
    assert result == expected


# Test censor_string function
@pytest.mark.parametrize(
    "test_id, string, expected",
    [
        ("happy-1", "SensitiveData", "Se***********"),
        ("edge-1", "", ""),
        ("edge-2", "AB", "AB"),
        ("edge-3", "A", "A"),
    ],
)
def test_censor_string(test_id, string, expected):  # noqa: D103, ARG001
    # Act
    result = censor_string(string)

    # Assert
    assert result == expected
