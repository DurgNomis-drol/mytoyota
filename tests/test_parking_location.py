"""pytest tests for mytoyota.location.ParkingLocation"""

from mytoyota.location import ParkingLocation  # pylint: disable=import-error

# pylint: disable=no-self-use


class TestParkingLocation:
    """pytest functions to test ParkingLocation"""

    def test_parking_location(self):
        """Test ParkingLocation"""
        location = ParkingLocation({"timestamp": 987654, "lat": 1.234, "lon": 5.678})
        assert location.latitude == 1.234
        assert location.longitude == 5.678
        assert location.timestamp == 987654

    def test_parking_location_no_data(self):
        """Test ParkingLocation with no initialization data"""
        location = ParkingLocation({})
        assert location.latitude == 0.0
        assert location.longitude == 0.0
        assert location.timestamp == 0
