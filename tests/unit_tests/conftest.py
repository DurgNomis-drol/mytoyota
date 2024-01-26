"""Need for pytest or else it will cause an import error in pytest."""
from pathlib import Path

import pytest


@pytest.fixture
def data_folder(request) -> str:
    """Return the folder containing test files."""
    return f"{Path(request.module.__file__).parent}/data"
