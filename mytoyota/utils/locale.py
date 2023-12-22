"""Locale validation utilities."""

import contextlib

from langcodes import Language
from langcodes.tag_parser import LanguageTagError


def is_valid_locale(locale: str) -> bool:
    """Is locale string valid."""
    valid = False
    if locale:
        with contextlib.suppress(LanguageTagError):
            valid = Language.get(locale).is_valid()
    return valid
