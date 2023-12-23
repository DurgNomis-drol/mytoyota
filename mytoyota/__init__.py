"""Toyota Connected Services Client."""
import importlib.metadata as importlib_metadata

from .client import MyT  # pylint: disable=unused-import # NOQA

__version__ = importlib_metadata.version(__name__)
