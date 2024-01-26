"""Test Helper Utils."""
import pytest

from mytoyota.utils.helpers import add_with_none


# Parametrized test for happy path with various realistic test values
@pytest.mark.parametrize(
    "this, that, result",
    [
        pytest.param(1, None, 1),
        pytest.param(None, 1, 1),
        pytest.param(1, 1, 2),
        pytest.param(None, None, None),
    ],
)
def test_is_valid_locale_happy_path(this, that, result):  # noqa: D103
    assert result == add_with_none(this, that)
