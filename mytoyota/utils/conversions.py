"""Conversion utilities used"""
import logging

_LOGGER: logging.Logger = logging.getLogger(__package__)


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
