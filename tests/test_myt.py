"""pytest tests for mytoyota.client.MyT"""

import pytest

from mytoyota.client import MyT
from mytoyota.exceptions import (
    ToyotaInvalidUsername,
    ToyotaLocaleNotValid,
    ToyotaRegionNotSupported,
)

# pylint: disable=no-self-use


class TestMyT:
    """pytest functions to test MyT"""

    def test_myt(self):
        """Test an error free initialisation of MyT"""
        myt = MyT(
            username="user@domain.com",
            password="xxxxx",
            locale="en-gb",
            region="europe",
        )
        assert myt is not None
        assert myt.api is not None

    @pytest.mark.parametrize(
        "username",
        [None, "", "_invalid_"],
    )
    def test_myt_invalid_username(self, username):
        """Test an invalid username in MyT"""
        with pytest.raises(ToyotaInvalidUsername):
            _ = MyT(
                username=username, password="xxxxx", locale="en-gb", region="europe"
            )

    @pytest.mark.parametrize(
        "locale",
        [
            None,
            "",
            "invalid-locale",
            "da-en-dk-us",
        ],
    )
    def test_myt_invalid_locale(self, locale):
        """Test an invalid locale in MyT"""
        with pytest.raises(ToyotaLocaleNotValid):
            _ = MyT(
                username="user@domain.com",
                password="xxxxx",
                locale=locale,
                region="europe",
            )

    @pytest.mark.parametrize(
        "region",
        [
            None,
            "",
            "antartica",
            "mars",
        ],
    )
    def test_myt_unsupported_region(self, region):
        """Test an invalid region in MyT"""
        with pytest.raises(ToyotaRegionNotSupported):
            _ = MyT(
                username="user@domain.com",
                password="xxxxx",
                locale="en-gb",
                region=region,
            )

    def test_get_supported_regions(self):
        """Test the supported regions"""
        regions = MyT.get_supported_regions()
        assert regions is not None
        assert len(regions) > 0
        assert "europe" in regions
