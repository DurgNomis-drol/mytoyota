"""Toyota Connected Services API exceptions."""


class ToyotaLocaleNotValid(Exception):
    """Raise if locale string is not valid."""


class ToyotaLoginError(Exception):
    """Raise if a login error happens."""


class ToyotaHttpError(Exception):
    """Raise if http error happens."""


class ToyotaNoCarError(Exception):
    """Raise if 205 is returned (Means no car found)."""
