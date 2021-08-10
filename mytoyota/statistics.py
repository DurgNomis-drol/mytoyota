"""Statistics class"""
import logging
import arrow

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Statistics:
    """Class to hold statistical information."""

    def __init__(self, raw_statistics: dict, interval: str) -> None:

        self.formated: list = []

        if not raw_statistics:
            _LOGGER.error("No statistical information provided!")
            return

        if interval == "day":
            self.formated = self.add_date_to_bucket_day(raw_statistics["histogram"])

        if interval in ("week", "month"):
            self.formated = raw_statistics["histogram"]

        if interval == "isoweek":
            self.formated.append(self.add_bucket_to_isoweek(raw_statistics))

        if interval == "year":
            self.formated.append(self.add_year_to_bucket_year(raw_statistics))

    def get_data(self) -> list:
        """Return formated data."""
        return self.formated

    @staticmethod
    def add_date_to_bucket_day(days):
        """Adds date to bucket."""
        for day in days:
            year = day["bucket"]["year"]
            dayofyear = day["bucket"]["dayOfYear"]

            day["bucket"].update(
                {
                    "date": arrow.now()
                    .strptime("{} {}".format(dayofyear, year), "%j %Y")
                    .format("YYYY-MM-DD")
                }
            )

        return days

    @staticmethod
    def add_bucket_to_isoweek(isoweek):
        """Adds bucket to isoweek and formats it."""
        data: dict = {
            "bucket": {
                "year": arrow.now().format("YYYY"),
                "week": arrow.now().strftime("%V"),
                "week_start": isoweek["from"],
            },
            "data": isoweek["summary"],
        }

        return data

    @staticmethod
    def add_year_to_bucket_year(year):
        """Adds year to bucket."""
        data: dict = {
            "bucket": {
                "year": arrow.now().format("YYYY"),
            },
            "data": year["summary"],
        }

        return data
