"""Toyota Connected Services API constants."""


BUCKET = "bucket"
DAYOFYEAR = "dayOfYear"
PERIODE_START = "periode_start"
DATE = "date"
DATA = "data"
SUMMARY = "summary"
HISTOGRAM = "histogram"
UNIT = "unit"

DAY = "day"
WEEK = "week"
ISOWEEK = "isoweek"
MONTH = "month"
YEAR = "year"

METRIC = "metric"
IMPERIAL = "imperial"
IMPERIAL_LITERS = "imperial_liters"

# DATE FORMATS
DATE_FORMAT = "YYYY-MM-DD"

# HTTP
TIMEOUT = 15

RETURNED_BAD_REQUEST = "bad_request"

TME_B2C_ERR_CPSERVICES = "TME_B2C_ERR_CPSERVICES_GET_FAILURE"

INTERVAL_SUPPORTED = ["day", "week", "isoweek", "month", "year"]

BASE_HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Accept": "application/json, text/plain, */*",
    "Sec-Fetch-Dest": "empty",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/51.0.2704.103 Safari/537.36"
    ),
}

# Timestamps
UNLOCK_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
