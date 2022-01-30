"""pytest tests for mytoyota.models.location.ParkingLocation"""

from mytoyota.models.location import ParkingLocation  # pylint: disable=import-error

# pylint: disable=no-self-use


class TestParkingLocation:
    """pytest functions to test ParkingLocation"""

    def _create_example_parking_location(self):
        """Create an ParkingLocation with some predefined example data"""
        return ParkingLocation({"timestamp": 987654, "lat": 1.234, "lon": 5.678})

    def test_parking_location(self):
        """Test ParkingLocation"""
        location = self._create_example_parking_location()
        assert location.latitude == 1.234
        assert location.longitude == 5.678
        assert location.timestamp == 987654

    def test_parking_location_no_data(self):
        """Test ParkingLocation with no initialization data"""
        location = ParkingLocation({})
        assert location.latitude == 0.0
        assert location.longitude == 0.0
        assert location.timestamp is None
