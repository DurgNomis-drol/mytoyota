"""Log utilities"""


def censor(text) -> str:
    """
    Replaces characters in a str with the asterisks
    text: The text to censure.
    """
    char = "*"
    text = text if text else ""
    return text[0] + (len(text) - 1) * char if text else text


def censor_cookie(cookie) -> str:
    """
    Replaces characters in a str with the asterisks
    text: The text to censure.
    """
    string = cookie.split("=")
    return string[0] + "=" + censor(string[1])


def censor_vin(vin) -> str:
    """
    Replaces parts of the vin number with asterisks.
    """
    vin = vin if vin else ""
    return vin[:-8] + "********" if vin else vin


def censor_dict(dictionary) -> dict:
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
