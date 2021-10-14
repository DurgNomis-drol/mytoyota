"""pytest tests for mytoyota.status.Odometer"""

from mytoyota.status import Odometer

# pylint: disable=no-self-use


class TestOdometer:
    """pytest functions to test Odometer"""

    def _create_example_odometer(self):
        """Create an ParkingLocation with some predefined example data"""
        return Odometer({"mileage": 765, "mileage_unit": "km"})

    def test_odometer_km(self):
        """Test a mileage specified in km"""
        odo = self._create_example_odometer()
        assert odo.mileage == 765
        assert odo.unit == "km"

    def test_odometer_miles(self):
        """Test a mileage specified in miles"""
        odo = Odometer({"mileage": 345, "mileage_unit": "miles"})
        assert odo.mileage == 345
        assert odo.unit == "miles"

    def test_odometer_no_data(self):
        """Test Odometer with no initialization data"""
        odo = Odometer({})
        assert odo.mileage is None
        assert odo.unit is None

    def test_odometer_str(self):
        """Test Odometer converted to a str"""
        odo = self._create_example_odometer()
        string = str(odo)
        assert isinstance(string, (str))
        assert string == "{'mileage': 765, 'unit': 'km'}"

    def test_odometer_dict(self):
        """Test Odometer converted to a dictionary"""
        odo = self._create_example_odometer()
        dictionary = odo.as_dict()
        assert isinstance(dictionary, (dict))
        assert dictionary == {"mileage": 765, "unit": "km"}
