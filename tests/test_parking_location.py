"""pytest tests for mytoyota.location.ParkingLocation"""

from mytoyota.location import ParkingLocation  # pylint: disable=import-error

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
        assert location.timestamp == 0

    def test_parking_location_str(self):
        """Test ParkingLocation converted to a str"""
        location = self._create_example_parking_location()
        string = str(location)
        assert isinstance(string, (str))
        assert string == "{'latitude': 1.234, 'longitude': 5.678, 'timestamp': 987654}"

    def test_parking_location_dict(self):
        """Test ParkingLocation converted to a dictionary"""
        location = self._create_example_parking_location()
        dictionary = location.as_dict()
        assert isinstance(dictionary, (dict))
        assert dictionary == {
            "timestamp": 987654,
            "latitude": 1.234,
            "longitude": 5.678,
        }
