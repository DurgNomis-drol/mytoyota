"""Statistics class"""
import logging

import arrow
from arrow import Arrow

from mytoyota.const import (
    BUCKET,
    DATA,
    DATE,
    DATE_FORMAT,
    DATE_FORMAT_YEAR,
    DAY,
    DAYOFYEAR,
    HISTOGRAM,
    ISOWEEK,
    MONTH,
    PERIODE_START,
    SUMMARY,
    WEEK,
    YEAR,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Statistics:  # pylint: disable=too-few-public-methods)
    """Class to hold statistical information."""

    def __init__(self, raw_statistics: dict, interval: str) -> None:

        self._now: Arrow = arrow.now()

        if not raw_statistics:
            _LOGGER.error("No statistical information provided!")
            return

        self._statistic = self._make_bucket(raw_statistics, interval)

    def as_list(self) -> list:
        """Return formatted data."""
        return self._statistic

    def _make_bucket(self, data: dict, interval: str) -> list:
        """Make bucket."""

        if interval is DAY:
            for day in data[HISTOGRAM]:
                year = day[BUCKET][YEAR]
                dayofyear = day[BUCKET][DAYOFYEAR]

                day[BUCKET].update(
                    {
                        DATE: self._now.strptime(
                            "{} {}".format(dayofyear, year), "%j %Y"
                        ).format(DATE_FORMAT),
                    }
                )
            return data[HISTOGRAM]

        if interval is ISOWEEK:
            data_with_bucket: dict = {
                BUCKET: {
                    YEAR: self._now.format(DATE_FORMAT_YEAR),
                    WEEK: self._now.strftime("%V"),
                    PERIODE_START: data["from"],
                },
                DATA: data[SUMMARY],
            }
            return [data_with_bucket]

        if interval is MONTH:
            for month in data[HISTOGRAM]:
                month[BUCKET].update(
                    {
                        PERIODE_START: self._now.replace(
                            year=month[BUCKET][YEAR], month=month[BUCKET][MONTH]
                        )
                        .floor(MONTH)
                        .format(DATE_FORMAT),
                    }
                )
            return data[HISTOGRAM]

        if interval is YEAR:
            data_with_bucket: dict = {
                BUCKET: {
                    YEAR: self._now.format(DATE_FORMAT_YEAR),
                    PERIODE_START: data["from"],
                },
                DATA: data[SUMMARY],
            }
            return [data_with_bucket]

        return data[HISTOGRAM]
