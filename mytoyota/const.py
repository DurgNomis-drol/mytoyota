"""Toyota Connected Services API constants."""

# URL ATTRIBUTE NAMES
ACCESS_TOKEN_URL = "access_token_url"
AUTHENTICATE_URL = "authenticate_url"
AUTHORIZE_URL = "authorize_url"
API_URL = "api_endpoint_url"
BASE_URL = "base_url"

# REGIONS
SUPPORTED_REGIONS = {
    "europe": {
        ACCESS_TOKEN_URL: "https://b2c-login.toyota-europe.com/oauth2/realms/root/realms/tme/access_token",
        AUTHENTICATE_URL: "https://b2c-login.toyota-europe.com/json/realms/root/realms/tme/authenticate?authIndexType=service&authIndexValue=oneapp",
        AUTHORIZE_URL: "https://b2c-login.toyota-europe.com/oauth2/realms/root/realms/tme/authorize?client_id=oneapp&scope=openid profile write&response_type=code&redirect_uri=com.toyota.oneapp:/oauth2Callback&code_challenge=plain&code_challenge_method=plain",
        API_URL: "https://ctpa-oneapi.tceu-ctp-prd.toyotaconnectedeurope.io",
        BASE_URL: "https://ctpa-oneapi.tceu-ctp-prd.toyotaconnectedeurope.io",
    }
}

# So we don't have to test the token if multiple endpoints is requested at the same time.
TOKEN_DURATION = 900
TOKEN_LENGTH = 114

# JSON ATTRIBUTES
TOKEN = "token"
UUID = "uuid"
CUSTOMERPROFILE = "customerProfile"
ACQUISITIONDATE = "AcquisitionDatetime"

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
