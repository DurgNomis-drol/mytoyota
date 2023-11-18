"""pytest tests for mytoyota.statistics.Statistics"""

# A lot of the code in the mytoyota.statistics.Statistics class is already
# tested by the unittests of the MyT.get_driving_statistics function.
# These pytest tests are only to test the strange cases

import pytest  # pylint: disable=import-error

from mytoyota.statistics import Statistics


class TestStatistics:
    """pytest functions to test Statistics"""

    def test_none_raw_statistics(self):
        """Test the initialization when None raw_statistics is provided"""
        stat = Statistics(None, "day")
        assert stat is not None
        with pytest.raises(AttributeError):
            assert stat.as_list() is None
