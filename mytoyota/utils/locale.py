"""Locale validation utilities"""
from langcodes import Language
from langcodes.tag_parser import LanguageTagError


def is_valid_locale(locale: str) -> bool:
    """Is locale string valid."""
    valid = False
    if locale:
        try:
            valid = Language.get(locale).is_valid()
        except LanguageTagError:
            pass
    return valid
