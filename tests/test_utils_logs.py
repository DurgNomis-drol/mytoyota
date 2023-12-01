"""pytest tests for mytoyota.utils.logs."""

from mytoyota.utils.logs import censor_all, censor_string


class TestLogUtilities:
    """pytest functions for testing logs."""

    def test_censor(self):
        """Testing sensitive info censoring."""
        string = censor_string("5957a713-f80f-483f-998c-97f956367048")

        assert string == "5***********************************"

    def test_censor_no_data(self):
        """Testing sensitive info censoring."""
        string = censor_string("")

        assert string == ""

    def test_censor_string(self):
        """Test censor_string."""
        vin = censor_string("JTDKGNEC00N999999")

        assert vin == "JTDKGNEC0********"

    def test_censor_string_no_data(self):
        """Test censor_string."""
        vin = censor_string("")

        assert vin == ""

    def test_censor_all(self):
        """Test censor_all."""
        dictionary = censor_all(
            {
                "vin": "JTDKGNEC00N999999",
                "VIN": "JTDKGNEC00N999999",
                "X-TME-TOKEN": "5957a713-f80f-483f-998c-97f956367048",
                "uuid": "ba1ba6cb-b3c9-47d1-a657-c28a05cdd66e",
                "id": 2199911,
                "Cookie": "iPlanetDirectoryPro=5957a713-f80f-483f-998c-97f956367048",
                "Today": "Tomorrow Toyota",
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
            "Today": "Tomorrow Toyota",
        }

    def test_censor_all_no_data(self):
        """Test censor_all with no data."""
        dictionary = censor_all({})

        assert isinstance(dictionary, dict)
        assert not dictionary
