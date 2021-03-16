"""Toyota Connected Services API exceptions."""


class ToyotaLocaleNotValid(Exception):
    """Raise if locale string is not valid."""


class ToyotaLoginError(Exception):
    """Raise if a login error happens."""


class ToyotaInvalidToken(Exception):
    """Raise if token is invalid"""


class ToyotaInvalidUsername(Exception):
    """Raise if username is invalid"""


class ToyotaRegionNotSupported(Exception):
    """Raise if region is not supported"""
