"""pytest tests for pytoyoda.__init__."""
from pytoyoda import MyT


def test_imports():
    """Ensure the imported module is the expected one."""
    assert MyT is not None
