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

# API URLs
API_BASE_URL = "HTTPS://ctpa-oneapi.tceu-ctp-prd.toyotaconnectedeurope.io"
ACCESS_TOKEN_URL = "HTTPS://b2c-login.toyota-europe.com/oauth2/realms/root/realms/tme/access_token"
AUTHENTICATE_URL = "HTTPS://b2c-login.toyota-europe.com/json/realms/root/realms/tme/authenticate?authIndexType=service&authIndexValue=oneapp"
AUTHORIZE_URL = "HTTPS://b2c-login.toyota-europe.com/oauth2/realms/root/realms/tme/authorize?client_id=oneapp&scope=openid+profile+write&response_type=code&redirect_uri=com.toyota.oneapp:/oauth2Callback&code_challenge=plain&code_challenge_method=plain"

# Endpoints
CUSTOMER_ACCOUNT_ENDPOINT = "TBD"
VEHICLE_ASSOCIATION_ENDPOINT = "/v1/vehicle-association/vehicle"
VEHICLE_GUID_ENDPOINT = "/v2/vehicle/guid"
VEHICLE_LOCATION_ENDPOINT = "/v1/location"
VEHICLE_HEALTH_STATUS_ENDPOINT = "/v1/vehiclehealth/status"
VEHICLE_GLOBAL_REMOTE_STATUS_ENDPOINT = "/v1/global/remote/status"
VEHICLE_GLOBAL_REMOTE_ELECTRIC_STATUS_ENDPOINT = "/v1/global/remote/electric/status"
VEHICLE_TELEMETRY_ENDPOINT = "/v3/telemetry"
VEHICLE_NOTIFICATION_HISTORY_ENDPOINT = "/v2/notification/history"
VEHICLE_TRIPS_ENDPOINT = "/v1/trips?from={from_date}&to={to_date}&route={route}&summary={summary}&limit={limit}&offset={offset}"  # noqa: E501

# Timestamps
UNLOCK_TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
