"""Toyota Connected Services API constants."""

# URL ATTRIBUTE NAMES
BASE_URL = "base_url"
BASE_URL_CARS = "base_url_cars"
ENDPOINT_AUTH = "auth_endpoint"

# REGIONS
SUPPORTED_REGIONS = {
    "europe": {
        BASE_URL: "https://myt-agg.toyota-europe.com/cma/api",
        BASE_URL_CARS: "https://cpb2cs.toyota-europe.com/vehicle",
        ENDPOINT_AUTH: "https://ssoms.toyota-europe.com/authenticate",
    }
}

TIMEOUT = 10

# LOGIN
USERNAME = "username"
PASSWORD = "password"

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

TOKEN_DURATION = 24 * 60 * 60
TOKEN_LENGTH = 114

# HTTP
HTTP_OK = 200
HTTP_NO_CONTENT = 204
HTTP_UNAUTHORIZED = 401
