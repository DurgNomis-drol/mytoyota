"""Toyota Connected Services API constants."""

# URL ATTRIBUTE NAMES
BASE_URL = "base_url"
BASE_URL_CARS = "base_url_cars"
ENDPOINT_AUTH = "auth_endpoint"
TOKEN_VALID_URL = "auth_valid"

# REGIONS
SUPPORTED_REGIONS = {
    "europe": {
        TOKEN_VALID_URL: "https://ssoms.toyota-europe.com/isTokenValid",
        BASE_URL: "https://myt-agg.toyota-europe.com/cma/api",
        BASE_URL_CARS: "https://cpb2cs.toyota-europe.com",
        ENDPOINT_AUTH: "https://ssoms.toyota-europe.com/authenticate",
    }
}

# LOGIN
USERNAME = "username"
PASSWORD = "password"

# So we don't have to test the token if multiple endpoints is requested at the same time.
TOKEN_DURATION = 900
TOKEN_LENGTH = 114

# JSON ATTRIBUTES
TOKEN = "token"
UUID = "uuid"
CUSTOMERPROFILE = "customerProfile"
FUEL = "fuel"
MILEAGE = "mileage"
TYPE = "type"
VALUE = "value"
UNIT = "unit"
VEHICLE_INFO = "VehicleInfo"
ACQUISITIONDATE = "AcquisitionDatetime"
CHARGE_INFO = "ChargeInfo"
HVAC = "RemoteHvacInfo"

BUCKET = "bucket"
DAYOFYEAR = "dayOfYear"
PERIODE_START = "periode_start"
DATE = "date"
DATA = "data"
SUMMARY = "summary"
HISTOGRAM = "histogram"

DAY = "day"
WEEK = "week"
ISOWEEK = "isoweek"
MONTH = "month"
YEAR = "year"

HOOD = "hood"
DOORS = "doors"
WINDOWS = "windows"
LIGHTS = "lamps"
KEY = "key"
CLOSED = "closed"
LOCKED = "locked"
WARNING = "warning"
STATE = "state"
OFF = "off"
INCAR = "inCar"

METRIC = "metric"
IMPERIAL = "imperial"
IMPERIAL_LITERS = "imperial_liters"

# DATE FORMATS
DATE_FORMAT_YEAR = "YYYY"
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
    "X-TME-BRAND": "TOYOTA",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}
