"""Toyota Connected Services API constants."""

# API URLs
API_BASE_URL = "HTTPS://ctpa-oneapi.tceu-ctp-prd.toyotaconnectedeurope.io"
ACCESS_TOKEN_URL = "HTTPS://b2c-login.toyota-europe.com/oauth2/realms/root/realms/tme/access_token"
AUTHENTICATE_URL = "HTTPS://b2c-login.toyota-europe.com/json/realms/root/realms/tme/authenticate?authIndexType=service&authIndexValue=oneapp"
AUTHORIZE_URL = "HTTPS://b2c-login.toyota-europe.com/oauth2/realms/root/realms/tme/authorize?client_id=oneapp&scope=openid+profile+write&response_type=code&redirect_uri=com.toyota.oneapp:/oauth2Callback&code_challenge=plain&code_challenge_method=plain"

# Endpoint URLs
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
VEHICLE_SERVICE_HISTORY_ENDPONT = "/v1/servicehistory/vehicle/summary"
