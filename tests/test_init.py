"""pytest tests for mytoyota.__init__."""
from mytoyota import MyT


def test_imports():
    """Ensure the imported module is the expected one."""
    assert MyT is not None
