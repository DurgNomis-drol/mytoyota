"""pytest tests for mytoyota.client.MyT using the online services"""

import asyncio

import pytest  # pylint: disable=import-error

from mytoyota.client import MyT
from mytoyota.exceptions import ToyotaLoginError

# pylint: disable=no-self-use


class TestMyTOnline:
    """pytest functions to test MyT using the online services"""

    def _create_online_myt(self, uuid=None) -> MyT:
        """Create a MyT instance that is using the OfflineController"""
        return MyT(
            username="username@domain.com",
            password="xxxxx",
            locale="en-gb",
            region="europe",
            uuid=uuid,
        )

    def test_login(self):
        """Test the login"""
        myt = self._create_online_myt()
        with pytest.raises(ToyotaLoginError):
            asyncio.run(myt.login())

    @pytest.mark.parametrize(
        "uuid",
        ["uuid1", "uuid2", "something", None],
    )
    def test_get_uuid(self, uuid):
        """Test the retrieval of an uuid"""
        myt = self._create_online_myt(uuid)
        actual_uuid = myt.uuid
        assert actual_uuid == uuid
