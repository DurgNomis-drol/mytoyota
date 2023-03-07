"""Formatters used"""
from typing import Dict, List


def format_odometer(raw: List) -> Dict:
    """Formats odometer information from a list to a dict."""
    instruments: dict = {}
    for instrument in raw:
        instruments[instrument["type"]] = instrument["value"]
        if "unit" in instrument:
            instruments[instrument["type"] + "_unit"] = instrument["unit"]

    return instruments
