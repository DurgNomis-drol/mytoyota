"""Toyota Connected Services API."""
from uuid import UUID
from langcodes import Language

from .const import TOKEN_LENGTH
from .exceptions import ToyotaInvalidToken


def is_valid_locale(locale: str) -> bool:
    """Is locale string valid."""
    return Language.make(locale).is_valid()


def is_valid_uuid(uuid_to_test, version=4):
    """Checks if uuid string is valid"""
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def is_valid_token(token):
    """Checks if token is the correct length"""
    if len(token) == TOKEN_LENGTH and token.endswith("..*"):
        return True

    raise ToyotaInvalidToken("Token must end with '..*' and be 114 characters long.")
