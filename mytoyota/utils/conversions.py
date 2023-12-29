"""Conversion utilities used."""
import logging

_LOGGER: logging.Logger = logging.getLogger(__package__)


def convert_to_miles(kilometers: float) -> float:
    """Convert kilometers to miles."""
    _LOGGER.debug(f"Converting {kilometers} to miles...")
    return kilometers * 0.621371192


def convert_to_km(miles: float) -> float:
    """Convert kilometers to miles."""
    _LOGGER.debug(f"Converting {miles} to kilometers...")
    return miles * 1.60934


def convert_distance(convert_to: str, convert_from: str, value: float, decimal_places: int = 3):
    """Convert distance for kilometers and miles."""
    if convert_to == convert_from:
        return round(value, decimal_places)
    if convert_to == "km":
        return round(convert_to_km(value), decimal_places)
    return round(convert_to_miles(value), decimal_places)


def convert_to_liter_per_100_miles(liters: float) -> float:
    """Convert liters per 100 km to liters per 100 miles."""
    _LOGGER.debug("Converting to L/100miles...")
    return round(liters * 1.609344, 4)


def convert_to_mpg(liters_per_100_km: float) -> float:
    """Convert to miles per UK gallon (MPG)."""
    _LOGGER.debug("Converting to MPG...")
    return round(282.5 / liters_per_100_km, 4) if liters_per_100_km > 0.0 else 0.0
