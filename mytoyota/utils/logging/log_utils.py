"""Utilities for manipulating returns for log output tasks."""
from typing import Any, Dict, Optional

from httpx import Response


def censor_value(value: Any, key: str, to_censor: set) -> Any:
    """Censor sensitive values in a given data structure.

    Args:
    ----
        value (Any): The value to be censored.
        key (str): The key associated with the value.
        to_censor (set): A set of keys to identify values that need to be censored.

    Returns:
    -------
        Any: The censored value.

    """
    if isinstance(value, str) and key.lower() in to_censor:
        return censor_string(value)
    if isinstance(value, float) and key.lower() in to_censor:
        return round(value)
    if isinstance(value, dict):
        return censor_all(value, to_censor)
    if isinstance(value, list):
        return [censor_value(item, key, to_censor) for item in value]
    return value


def format_httpx_response(response: Response) -> str:
    """Format an HTTPX response into a string representation.

    Args:
    ----
        response (Response): The HTTPX response object to format.

    Returns:
    -------
        str: The formatted representation of the HTTPX response.

    """
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


def censor_all(dictionary: Dict[str, Any], to_censor: Optional[set] = None) -> Dict[str, Any]:
    r"""Censor sensitive values in a dictionary.

    Args:
    ----
        dictionary (Dict[str, Any]): The dictionary to be censored.
        to_censor (Optional[set], optional): A set of keys to identify values \n
            that need to be censored. Defaults to None.

    Returns:
    -------
        Dict[str, Any]: The censored dictionary.

    """
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
            "katashiki_code",
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
    """Censor a string by replacing all characters except the first two with asterisks.

    Args:
    ----
        string (str): The string to be censored.

    Returns:
    -------
        str: The censored string.

    """
    return string[:2] + (len(string) - 2) * "*" if string else string
