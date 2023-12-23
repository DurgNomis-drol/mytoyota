"""Toyota Connected Services Client."""
from importlib.metadata import version

from .client import MyT  # pylint: disable=unused-import # NOQA

__version__ = version(__name__)
