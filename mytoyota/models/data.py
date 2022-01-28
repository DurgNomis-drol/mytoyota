"""Base data model."""
from typing import Any, Dict


class VehicleData:
    def __init__(self, data: dict) -> None:
        self._data = data or {}
    
    @property
    def raw_json(self) -> Dict[str, Any]:
        return self._data