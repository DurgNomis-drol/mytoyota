"""Base data model."""
from typing import Any, Dict


class VehicleData:
    """Vehicle data base model."""

    def __init__(self, data: dict) -> None:
        self._data = data or {}

    @property
    def raw_json(self) -> Dict[str, Any]:
        """Return the input data."""
        return self._data
