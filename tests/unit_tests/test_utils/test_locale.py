"""Test Locale Utils."""
import pytest

from pytoyoda.utils.locale import is_valid_locale


# Parametrized test for happy path with various realistic test values
@pytest.mark.parametrize(
    "locale, expected",
    [
        pytest.param("en-GB", True, id="id_valid_english_gb"),
        pytest.param("en-US", True, id="id_valid_english_us"),
        pytest.param("fr-FR", True, id="id_valid_french"),
        pytest.param("de-DE", True, id="id_valid_german"),
    ],
)
def test_is_valid_locale_happy_path(locale, expected):  # noqa: D103
    # Act
    result = is_valid_locale(locale)

    # Assert
    assert result == expected


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "locale, expected",
    [
        pytest.param("", False, id="id_empty_string"),
        pytest.param("en-GB-oed", True, id="id_valid_english_oxford"),
        pytest.param("i-klingon", True, id="id_valid_klingon"),  # Grandfathered tag
        pytest.param("x-private", True, id="id_valid_private_use"),  # Private use tag
    ],
)
def test_is_valid_locale_edge_cases(locale, expected):  # noqa: D103
    # Act
    result = is_valid_locale(locale)

    # Assert
    assert result == expected


# Parametrized test for error cases
@pytest.mark.parametrize(
    "locale, expected",
    [
        pytest.param("en-US-12345", False, id="id_invalid_subtag_length"),
        pytest.param("123-en", False, id="id_invalid_language_digits"),
        pytest.param("en@currency=USD", False, id="id_invalid_locale_with_currency"),
    ],
)
def test_is_valid_locale_error_cases(locale, expected):  # noqa: D103
    # Act
    result = is_valid_locale(locale)

    # Assert
    assert result == expected
