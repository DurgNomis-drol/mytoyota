"""pytest tests for mytoyota.utils"""
# pylint: disable=import-error
import pytest

from mytoyota.exceptions import ToyotaInvalidToken
from mytoyota.utils.conversions import (
    convert_to_liter_per_100_miles,
    convert_to_miles,
    convert_to_mpg,
)
from mytoyota.utils.formatters import format_odometer
from mytoyota.utils.locale import is_valid_locale


class TestUtils:
    """pytest functions to test functions in mytoyota.utils"""

    @pytest.mark.parametrize(
        "locale",
        [
            "en-us",
            "en-gb",
            "nl-nl",
            "da-dk",
        ],
    )
    def test_is_valid_locale(self, locale: str):
        """Test valid cases for is_valid_locale"""
        assert is_valid_locale(locale)

    @pytest.mark.parametrize(
        "invalid_locale",
        [
            "",
            None,
            "something_invalid",
            "en-u",
            "en-us-nl-nl",
        ],
    )
    def test_not_is_valid_locale(self, invalid_locale: str):
        """Test invalid cases for is_valid_locale"""
        assert not is_valid_locale(invalid_locale)


    @pytest.mark.parametrize(
        "distance_km,distance_miles",
        [
            (1, 0.6214),
            (0, 0),
            (1000, 621.3712),
        ],
    )
    def test_convert_to_miles(self, distance_km, distance_miles):
        """Test conversion from km to miles"""
        assert convert_to_miles(distance_km) == distance_miles

    @pytest.mark.parametrize(
        "liters_km,per_mile",
        [
            (1, 1.6093),
            (0, 0),
            (1000, 1609.344),
        ],
    )
    def test_convert_to_liter_per_100_miles(self, liters_km, per_mile):
        """Test conversion from l/100km to l/100miles"""
        assert convert_to_liter_per_100_miles(liters_km) == per_mile

    @pytest.mark.parametrize(
        "liters_km,mpg",
        [
            (0, 0),
            (0.01, 28250.0),
            (1, 282.5),
            (12, 23.5417),
        ],
    )
    def test_convert_to_mpg(self, liters_km, mpg):
        """Test conversion from liters/100km to miles per gallons"""
        assert convert_to_mpg(liters_km) == mpg

    def test_format_odometer(self):
        """Test format odometer"""

        raw = [
            {"type": "mileage", "value": 3205, "unit": "km"},
            {"type": "Fuel", "value": 22},
        ]

        formatted = format_odometer(raw)

        assert isinstance(formatted, dict)
        assert formatted == {
            "mileage": 3205,
            "mileage_unit": "km",
            "Fuel": 22,
        }

    def test_format_odometer_no_data(self):
        """Test format odometer with no initialization data"""

        nothing = format_odometer([])

        assert isinstance(nothing, dict)
        assert not nothing
