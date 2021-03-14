"""Toyota Connected Services API."""
from langcodes import Language


def locale_is_valid(locale: str) -> bool:
    """Is locale string valid."""
    return Language.make(locale).is_valid()
