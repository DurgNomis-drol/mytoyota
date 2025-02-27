"""Test Formatter Utils."""
import pytest

from pytoyoda.utils.formatters import format_odometer


# Test cases for the happy path with various realistic test values
@pytest.mark.parametrize(
    "test_input, expected",
    [
        (
            pytest.param(
                [{"type": "mileage", "value": 12345}],
                {"mileage": 12345},
                id="single_instrument_no_unit",
            )
        ),
        (
            pytest.param(
                [{"type": "mileage", "value": 12345, "unit": "km"}],
                {"mileage": 12345, "mileage_unit": "km"},
                id="single_instrument_with_unit",
            )
        ),
        (
            pytest.param(
                [
                    {"type": "mileage", "value": 12345, "unit": "km"},
                    {"type": "fuel", "value": 50, "unit": "liters"},
                ],
                {
                    "mileage": 12345,
                    "mileage_unit": "km",
                    "fuel": 50,
                    "fuel_unit": "liters",
                },
                id="multiple_instruments_with_units",
            )
        ),
    ],
)
def test_format_odometer_happy_path(test_input, expected):  # noqa: D103
    # Act
    result = format_odometer(test_input)

    # Assert
    assert result == expected


# Test cases for edge cases
@pytest.mark.parametrize(
    "test_input, expected",
    [
        (pytest.param([], {}, id="empty_list")),
        (pytest.param([{"type": "mileage", "value": 0}], {"mileage": 0}, id="zero_value")),
        (
            pytest.param(
                [
                    {"type": "mileage", "value": 12345},
                    {"type": "mileage", "value": 67890},
                ],
                {"mileage": 67890},
                id="duplicate_type_last_wins",
            )
        ),
    ],
)
def test_format_odometer_edge_cases(test_input, expected):  # noqa: D103
    # Act
    result = format_odometer(test_input)

    # Assert
    assert result == expected


# Test cases for error cases
@pytest.mark.parametrize(
    "test_input, expected_exception",
    [
        (pytest.param([{"value": 12345}], KeyError, id="missing_type_key")),
        (pytest.param([{"type": "mileage"}], KeyError, id="missing_value_key")),
        (pytest.param("not_a_list", TypeError, id="non_list_input")),
        (pytest.param([12345], TypeError, id="non_dict_in_list")),
    ],
)
def test_format_odometer_error_cases(test_input, expected_exception):  # noqa: D103
    # Act / Assert
    with pytest.raises(expected_exception):
        format_odometer(test_input)
