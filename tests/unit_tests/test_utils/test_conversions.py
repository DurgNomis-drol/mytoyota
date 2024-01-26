"""Test Conversion Utils."""
import pytest

from mytoyota.utils import conversions


# Test for convert_to_miles
@pytest.mark.parametrize(
    "kilometers, expected_miles",
    [
        pytest.param(1, 0.621, id="1km_to_miles"),
        pytest.param(0, 0.0, id="0km_to_miles"),
        pytest.param(10, 6.214, id="10km_to_miles"),
        pytest.param(-1, -0.621, id="negative_km_to_miles"),
    ],
)
def test_convert_to_miles(kilometers, expected_miles):  # noqa: D103
    # Act
    miles = conversions.convert_to_miles(kilometers)

    # Assert
    assert round(miles, 3) == expected_miles


# Test for convert_to_km
@pytest.mark.parametrize(
    "miles, expected_km",
    [
        pytest.param(1, 1.609, id="1mile_to_km"),
        pytest.param(0, 0.0, id="0mile_to_km"),
        pytest.param(10, 16.093, id="10miles_to_km"),
        pytest.param(-1, -1.609, id="negative_mile_to_km"),
    ],
)
def test_convert_to_km(miles, expected_km):  # noqa: D103
    # Act
    km = conversions.convert_to_km(miles)

    # Assert
    assert round(km, 3) == expected_km


# Test for convert_distance
@pytest.mark.parametrize(
    "convert_to, convert_from, value, decimal_places, expected",
    [
        pytest.param("km", "miles", 1, 3, 1.609, id="1mile_to_km"),
        pytest.param("miles", "km", 1, 3, 0.621, id="1km_to_miles"),
        pytest.param("km", "km", 1, 3, 1.000, id="1km_to_km"),
        pytest.param("miles", "miles", 1, 3, 1.000, id="1mile_to_mile"),
        pytest.param("km", "miles", 0, 3, 0.0, id="0mile_to_km"),
        pytest.param("miles", "km", 0, 3, 0.0, id="0km_to_miles"),
        pytest.param("km", "miles", 1, 0, 2, id="1mile_to_km_no_decimals"),
        pytest.param("miles", "km", 1, 0, 1, id="1km_to_miles_no_decimals"),
        pytest.param("km", "miles", -1, 3, -1.609, id="negative_mile_to_km"),
        pytest.param("miles", "km", -1, 3, -0.621, id="negative_km_to_miles"),
    ],
)
def test_convert_distance(  # noqa: D103
    convert_to, convert_from, value, decimal_places, expected
):
    # Act
    result = conversions.convert_distance(convert_to, convert_from, value, decimal_places)

    # Assert
    assert result == expected


# Test for convert_to_liter_per_100_miles
@pytest.mark.parametrize(
    "liters, expected",
    [
        pytest.param(1, 1.6093, id="1liter_to_100miles"),
        pytest.param(0, 0.0, id="0liter_to_100miles"),
        pytest.param(10, 16.0934, id="10liters_to_100miles"),
        pytest.param(-1, -1.6093, id="negative_liter_to_100miles"),
    ],
)
def test_convert_to_liter_per_100_miles(liters, expected):  # noqa: D103
    # Act
    result = conversions.convert_to_liter_per_100_miles(liters)

    # Assert
    assert result == expected


# Test for convert_to_mpg
@pytest.mark.parametrize(
    "liters_per_100_km, expected_mpg",
    [
        pytest.param(1, 282.5000, id="1liter_to_mpg"),
        pytest.param(0, 0.0, id="0liter_to_mpg"),
        pytest.param(10, 28.2500, id="10liters_to_mpg"),
        pytest.param(5.5, 51.3636, id="5.5liters_to_mpg"),
        pytest.param(-1, 0.0, id="negative_liter_to_mpg"),
    ],
)
def test_convert_to_mpg(liters_per_100_km, expected_mpg):  # noqa: D103
    # Act
    mpg = conversions.convert_to_mpg(liters_per_100_km)

    # Assert
    assert mpg == expected_mpg
