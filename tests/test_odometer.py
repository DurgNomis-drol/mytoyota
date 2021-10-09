"""pytest tests for mytoyota.status.Odometer"""

from mytoyota.status import Odometer

# pylint: disable=no-self-use


class TestOdometer:
    """pytest functions to test Odometer"""

    def test_odometer_km(self):
        """Test a mileage specified in km"""
        odo = Odometer({"mileage": 765, "mileage_unit": "km"})
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
