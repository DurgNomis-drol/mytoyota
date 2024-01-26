"""Test mytoyota client."""
import pytest

from mytoyota.client import MyT
from mytoyota.exceptions import ToyotaInvalidUsernameError

# Constants for tests
VALID_USERNAME = "user@example.com"
VALID_PASSWORD = "securepassword123"
INVALID_USERNAME = "userexample.com"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, expected_exception, test_id",
    [
        (VALID_USERNAME, VALID_PASSWORD, None, "happy_path_valid_credentials"),
        (
            INVALID_USERNAME,
            VALID_PASSWORD,
            ToyotaInvalidUsernameError,
            "error_invalid_username",
        ),
    ],
)
async def test_myt_init(  # noqa : D103
    username,
    password,
    expected_exception,
    test_id,  # noqa : ARG001
):
    # Arrange
    if expected_exception:
        with pytest.raises(expected_exception):
            MyT(username, password)
    else:
        # Act
        client = MyT(username, password)
        # Assert
        assert client._api is not None
