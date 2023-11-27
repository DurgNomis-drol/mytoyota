from typing import Any


def censor_value(value: Any, key: str, to_censor: set) -> Any:
    if isinstance(value, str) and key.lower() in to_censor:
        return censor(value)
    elif isinstance(value, float) and key.lower() in to_censor:
        return round(value)
    elif isinstance(value, dict):
        return censor_all(value, to_censor)
    elif isinstance(value, list):
        return [censor_value(item, key, to_censor) for item in value]
    return value


def censor_all(dictionary: dict[str, Any], to_censor: set = None) -> dict[str, Any]:
    if to_censor is None:
        to_censor = {
            "vin",
            "uuid",
            "guid",
            "x-guid",
            "authorization",
            "latitude",
            "longitude",
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
        }
    return {k: censor_value(v, k, to_censor) for k, v in dictionary.items()}


def censor(text: str) -> str:
    return text[:2] + (len(text) - 2) * "*" if text else text


def censor_cookie(cookie: str) -> str:
    string = cookie.split("=")
    return f"{string[0]}={censor(string[1])}"


def censor_vin(vin: str) -> str:
    return f"{vin[:-8]}********" if vin else vin
