"""Toyota Connected Services API."""
import logging

from langcodes import Language
from langcodes.tag_parser import LanguageTagError

from .const import TOKEN_LENGTH
from .exceptions import ToyotaInvalidToken

_LOGGER: logging.Logger = logging.getLogger(__package__)


def is_valid_locale(locale: str) -> bool:
    """Is locale string valid."""
    valid = False
    if locale:
        try:
            valid = Language.get(locale).is_valid()
        except LanguageTagError:
            pass
    return valid


def is_valid_token(token: str) -> bool:
    """Checks if token is the correct length"""
    if len(token) == TOKEN_LENGTH and token.endswith("..*"):
        return True

    raise ToyotaInvalidToken("Token must end with '..*' and be 114 characters long.")


def format_odometer(raw: list) -> dict:
    """Formats odometer information from a list to a dict."""
    instruments: dict = {}
    for instrument in raw:
        instruments[instrument["type"]] = instrument["value"]
        if "unit" in instrument:
            instruments[instrument["type"] + "_unit"] = instrument["unit"]

    return instruments


def convert_to_miles(kilometers: float) -> float:
    """Convert kilometers to miles"""
    _LOGGER.debug(f"Converting {kilometers} to miles...")
    return round(kilometers * 0.621371192, 4)


def convert_to_liter_per_100_miles(liters: float) -> float:
    """Convert liters per 100 km to liters per 100 miles"""
    _LOGGER.debug("Converting to L/100miles...")
    return round(liters * 1.609344, 4)


def convert_to_mpg(liters_per_100_km: float) -> float:
    """Convert to miles per UK gallon (MPG)"""
    _LOGGER.debug("Converting to MPG...")
    if liters_per_100_km > 0.0:
        return round(282.5 / liters_per_100_km, 4)
    return 0.0
