"""Toyota Connected Services API."""
from langcodes import Language

from .const import TOKEN_LENGTH
from .exceptions import ToyotaInvalidToken


def is_valid_locale(locale: str) -> bool:
    """Is locale string valid."""
    return Language.make(locale).is_valid()


def is_valid_token(token):
    """Checks if token is the correct length"""
    if len(token) == TOKEN_LENGTH and token.endswith("..*"):
        return True

    raise ToyotaInvalidToken("Token must end with '..*' and be 114 characters long.")
