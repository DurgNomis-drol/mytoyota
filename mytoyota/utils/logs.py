"""Log utilities"""
from typing import Any


def censor(text: str) -> str:
    """
    Replaces characters in a str with the asterisks
    text: The text to censure.
    """
    char = "*"
    text = text or ""
    return text[:2] + (len(text) - 2) * char if text else text


def censor_cookie(cookie: str) -> str:
    """
    Replaces characters in a str with the asterisks
    text: The text to censure.
    """
    string = cookie.split("=")
    return f"{string[0]}={censor(string[1])}"


def censor_vin(vin: str) -> str:
    """
    Replaces parts of the vin number with asterisks.
    """
    vin = vin or ""
    return f"{vin[:-8]}********" if vin else vin


def censor_dict(dictionary: dict[str, Any]) -> dict[str, Any]:
    # TODO combine this with censor_all
    """
    Censors token, vin and other private info in a dict.
    """
    if "vin" in dictionary:
        dictionary["vin"] = censor_vin(dictionary["vin"])

    if "VIN" in dictionary:
        dictionary["VIN"] = censor_vin(dictionary["VIN"])

    if "X-TME-TOKEN" in dictionary:
        dictionary["X-TME-TOKEN"] = censor(dictionary["X-TME-TOKEN"])

    if "uuid" in dictionary:
        dictionary["uuid"] = censor(dictionary["uuid"])

    if "id" in dictionary:
        dictionary["id"] = censor(str(dictionary["id"]))

    if "Cookie" in dictionary:
        dictionary["Cookie"] = censor_cookie(dictionary["Cookie"])

    return dictionary


def censor_all(dictionary: dict[str, Any]) -> dict[str, Any]:
    to_censor = [
        "vin",
        "uuid",
        "guid",
        "x-guid",
        "authorization",
        "latitude",
        "longitude",
        "emergencyContact",
        "remoteuserguid",
        "subscriberguid",
        "contractId",
        "imei",
        "katashikiCode",
        "subscriptionID",
    ]

    for k, v in dictionary.items():
        if isinstance(v, dict):
            dictionary[k] = censor_all(v)
        elif isinstance(v, list):
            for l in v:
                if isinstance(l, dict):
                    dictionary[k] = censor_all(l)
        elif k.lower() in to_censor:
            if isinstance(v, str):
                dictionary[k] = censor(v)
            elif isinstance(v, float):
                dictionary[k] = round(v)
            else:
                print(k, v, type(v))

    return dictionary
