from typing import Any, Dict, Optional

from httpx import Response


def censor_value(value: Any, key: str, to_censor: set) -> Any:
    if isinstance(value, str) and key.lower() in to_censor:
        return censor_string(value)
    elif isinstance(value, float) and key.lower() in to_censor:
        return round(value)
    elif isinstance(value, dict):
        return censor_all(value, to_censor)
    elif isinstance(value, list):
        return [censor_value(item, key, to_censor) for item in value]
    return value


def format_httpx_response(response: Response) -> str:
    return (
        f"Request:\n"
        f"  Method : {response.request.method}\n"
        f"  URL    : {response.request.url}\n"
        f"  Headers: {response.request.headers}\n"
        f"  Body   : {response.request.content.decode('utf-8')}\n"
        f"Response:\n"
        f"  Status : ({response.status_code},{response.reason_phrase})\n"
        f"  Headers: {response.headers}\n"
        f"  Content: {response.content.decode('utf-8')}"
    )


def censor_all(
    dictionary: Dict[str, Any], to_censor: Optional[set] = None
) -> Dict[str, Any]:
    if to_censor is None:
        to_censor = {
            "vin",
            "uuid",
            "guid",
            "x-guid",
            "authorization",
            "latitude",
            "longitude",
            "link",
            "emergencycontact",
            "remoteuserguid",
            "subscriberguid",
            "contractid",
            "imei",
            "katashikicode",
            "subscriptionid",
            "cookie",
            "x-tme-token",
            "id",
            "subscription_id",
            "phone_number",
            "phone_numbers",
            "email_address",
            "emails",
            "first_name",
            "lastname",
            "euicc_id",
            "contract_id",
            "start_lat",
            "start_lon",
            "end_lat",
            "end_lon",
            "lat",
            "lon",
        }
    return {k: censor_value(v, k, to_censor) for k, v in dictionary.items()}


def censor_string(string: str) -> str:
    return string[:2] + (len(string) - 2) * "*" if string else string


def censor_cookie(cookie: str) -> str:
    string = cookie.split("=")
    return f"{string[0]}={censor_string(string[1])}"


def censor_vin(vin: str) -> str:
    return f"{vin[:-8]}********" if vin else vin
