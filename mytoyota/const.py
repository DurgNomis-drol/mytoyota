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

# HTTP
TIMEOUT = 10

HTTP_OK = 200
HTTP_NO_CONTENT = 204
HTTP_UNAUTHORIZED = 401
