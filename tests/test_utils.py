"""pytest tests for mytoyota.utils"""

import pytest  # pylint: disable=import-error

from mytoyota.exceptions import ToyotaInvalidToken
from mytoyota.utils import (
    convert_to_liter_per_100_miles,
    convert_to_miles,
    convert_to_mpg,
    is_valid_locale,
    is_valid_token,
)

# pylint: disable=no-self-use


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
        "token",
        [
            "T" * 111 + "..*",
            "0" * 111 + "..*",
            "." * 111 + "..*",
        ],
    )
    def test_is_valid_token(self, token: str):
        """Test valid cases for is_valid_token"""
        assert is_valid_token(token)

    @pytest.mark.parametrize(
        "invalid_token",
        [
            "..*",
            "234234.*",
            "234234..",
            "234234",
            "0" * 110 + "..*",
            "." * 112 + "..*",
            None,
            "",
        ],
    )
    def test_not_is_valid_token(self, invalid_token: str):
        """Test invalid cases for is_valid_token"""
        with pytest.raises(ToyotaInvalidToken):
            is_valid_token(invalid_token)

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
            (1, 282.5),
            # Joro75: A divide by zero is triggered!!
            # (0, 0),
            (12, 23.5417),
        ],
    )
    def test_convert_to_mpg(self, liters_km, mpg):
        """Test conversion from liters/100km to miles per gallons"""
        assert convert_to_mpg(liters_km) == mpg
