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
    IMPERIAL,
    IMPERIAL_LITERS,
    ISOWEEK,
    METRIC,
    MONTH,
    PERIODE_START,
    SUMMARY,
    UNIT,
    WEEK,
    YEAR,
)
from mytoyota.utils.conversions import (
    convert_to_liter_per_100_miles,
    convert_to_miles,
    convert_to_mpg,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Statistics:
    """Class to hold statistical information."""

    def __init__(
        self,
        raw_statistics: dict,
        interval: str,
        imperial: bool = False,
        use_liters: bool = False,
    ) -> None:

        self._now: Arrow = arrow.now()

        if not raw_statistics:
            _LOGGER.error("No statistical information provided!")
            return

        stats_as_list = self._add_bucket(raw_statistics, interval)

        if imperial:
            stats_as_list = self._convert_to_imperial(stats_as_list, use_liters)

        self._statistic = stats_as_list

    def as_list(self) -> list:
        """Return formatted data."""
        return self._statistic

    @staticmethod
    def _convert_to_imperial(data: list, use_liters: bool) -> list:
        """
        Toyota converts some of the data, but not all for some reason. This function
        corrects these values and adds the possibility to show them in MPG also.
        """

        _LOGGER.debug("Converting statistics to imperial...")

        attributes_to_convert = [
            "evDistanceInKm",
            "totalDistanceInKm",
            "maxSpeedInKmph",
            "averageSpeedInKmph",
            "highwayDistanceInKm",
            "totalFuelConsumedInL",
        ]

        for periode in data:
            periode[BUCKET].update(
                {
                    UNIT: IMPERIAL_LITERS if use_liters else IMPERIAL,
                }
            )
            for attribute in attributes_to_convert:
                if attribute in periode[DATA]:
                    if attribute == "totalFuelConsumedInL":
                        _LOGGER.debug(f"Converting attribute {attribute}...")
                        periode[DATA][attribute] = (
                            convert_to_liter_per_100_miles(periode[DATA][attribute])
                            if use_liters
                            else convert_to_mpg(periode[DATA][attribute])
                        )
                        continue

                    _LOGGER.debug(f"Converting attribute {attribute} to miles...")
                    periode[DATA][attribute] = convert_to_miles(
                        periode[DATA][attribute]
                    )
        return data

    def _add_bucket(self, data: dict, interval: str) -> list:
        """Add bucket and return statistics in a uniform way."""

        _LOGGER.debug("Updating bucket for statistics....")

        if interval is DAY:
            for day in data[HISTOGRAM]:
                year = day[BUCKET][YEAR]
                dayofyear = day[BUCKET][DAYOFYEAR]

                day[BUCKET].update(
                    {
                        UNIT: METRIC,
                        DATE: self._now.strptime(f"{dayofyear} {year}", "%j %Y").format(
                            DATE_FORMAT
                        ),
                    }
                )
            return data[HISTOGRAM]

        if interval is ISOWEEK:
            data_with_bucket: dict = {
                BUCKET: {
                    YEAR: self._now.format(DATE_FORMAT_YEAR),
                    WEEK: self._now.strftime("%V"),
                    UNIT: METRIC,
                    PERIODE_START: data["from"],
                },
                DATA: data[SUMMARY],
            }
            return [data_with_bucket]

        if interval is MONTH:
            for month in data[HISTOGRAM]:
                month[BUCKET].update(
                    {
                        UNIT: METRIC,
                        PERIODE_START: self._now.replace(
                            year=month[BUCKET][YEAR], month=month[BUCKET][MONTH], day=1
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
                    UNIT: METRIC,
                    PERIODE_START: data["from"],
                },
                DATA: data[SUMMARY],
            }
            return [data_with_bucket]

        for periode in data[HISTOGRAM]:
            periode[BUCKET].update(
                {
                    UNIT: METRIC,
                }
            )

        return data[HISTOGRAM]
