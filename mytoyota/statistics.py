"""Statistics class"""
import logging

import arrow

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Statistics:
    """Class to hold statistical information."""

    def __init__(self, raw_statistics: dict, interval: str) -> None:

        self.raw: dict = {}

        if not raw_statistics:
            _LOGGER.error("No statistical information provided!")
            return

        if interval in ("day", "week", "month"):
            self.raw = raw_statistics["histogram"][0]

        if interval == "isoweek":
            self.raw["bucket"] = {
                "year": arrow.now().format("YYYY"),
                "week": arrow.now().strftime("%V"),
            }
            self.raw["data"] = raw_statistics["summary"]

        if interval == "year":
            self.raw["bucket"] = {
                "year": arrow.now().format("YYYY"),
            }
            self.raw["data"] = raw_statistics["summary"]

    def __str__(self) -> str:
        """Return as string."""
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return self.raw
