"""pytest tests for mytoyota.utils.logs"""

from mytoyota.utils.logs import censor, censor_dict, censor_location, censor_vin

# pylint: disable=no-self-use


class TestLogUtilities:
    """pytest functions for testing logs"""

    def test_censor(self):
        """Testing sensitive info censoring"""
        string = censor("5957a713-f80f-483f-998c-97f956367048")

        assert string == "5***********************************"

    def test_censor_no_data(self):
        """Testing sensitive info censoring"""
        string = censor("")

        assert string == ""

    def test_censor_vin(self):
        """Test censor_vin"""
        vin = censor_vin("JTDKGNEC00N999999")

        assert vin == "JTDKGNEC0********"

    def test_censor_vin_no_data(self):
        """Test censor_vin"""
        vin = censor_vin("")

        assert vin == ""

    def test_censor_location(self):
        """Test censor_location"""
        location = censor_location({"timestamp": 987654, "lat": 1.234, "lon": 5.678})

        assert location["lat"] == "********"
        assert location["lon"] == "********"
        assert location["timestamp"] == 987654

    def test_censor_location_no_data(self):
        """Test censor_location"""
        location = censor_location({})

        assert isinstance(location, dict)
        assert location == {}

    def test_censor_dict(self):
        """Test censor_dict"""

        dictionary = censor_dict(
            {
                "vin": "JTDKGNEC00N999999",
                "VIN": "JTDKGNEC00N999999",
                "X-TME-TOKEN": "5957a713-f80f-483f-998c-97f956367048",
                "uuid": "ba1ba6cb-b3c9-47d1-a657-c28a05cdd66e",
                "id": 2199911,
                "Cookie": "iPlanetDirectoryPro=5957a713-f80f-483f-998c-97f956367048",
            }
        )

        assert isinstance(dictionary, dict)
        assert dictionary == {
            "vin": "JTDKGNEC0********",
            "VIN": "JTDKGNEC0********",
            "X-TME-TOKEN": "5***********************************",
            "uuid": "b***********************************",
            "id": "2******",
            "Cookie": "iPlanetDirectoryPro=5***********************************",
        }

    def test_censor_dict_no_data(self):
        """Test censor_dict with no data"""

        dictionary = censor_dict({})

        assert isinstance(dictionary, dict)
        assert dictionary == {}
