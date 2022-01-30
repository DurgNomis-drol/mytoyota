"""pytest tests for mytoyota.models.hvac.Hvac"""

from mytoyota.models.hvac import Hvac

# pylint: disable=no-self-use


class TestHvac:
    """pytest functions to test Hvac"""

    @staticmethod
    def _create_example_data():
        """Create hvac with predefined data"""
        return Hvac(
            {
                "currentTemperatureIndication": {
                    "timestamp": "2020-10-16T03:50:15Z",
                    "unit": "string",
                    "value": 22,
                },
                "targetTemperature": {
                    "timestamp": "2020-10-16T03:50:15Z",
                    "unit": "string",
                    "value": 21,
                },
                "startedAt": "",
                "status": "",
                "type": "",
                "duration": 1,
                "options": {
                    "frontDefogger": "",
                    "frontDriverSeatHeater": "",
                    "frontPassengerSeatHeater": "",
                    "mirrorHeater": "",
                    "rearDefogger": "",
                    "rearDriverSeatHeater": "",
                    "rearPassengerSeatHeater": "",
                    "steeringHeater": "",
                },
                "commandId": "",
            }
        )

    @staticmethod
    def _create_example_legacy_data():
        """Create legacy hvac with predefined data"""
        return Hvac(
            {
                "BlowerStatus": 0,
                "FrontDefoggerStatus": 0,
                "InsideTemperature": 22,
                "LatestAcStartTime": "2020-10-16T03:50:15Z",
                "RearDefoggerStatus": 0,
                "RemoteHvacMode": 0,
                "RemoteHvacProhibitionSignal": 1,
                "SettingTemperature": 21,
                "TemperatureDisplayFlag": 0,
                "Temperaturelevel": 29,
            },
            legacy=True,
        )

    def test_hvac(self):
        """Test Hvac"""
        hvac = self._create_example_data()

        assert hvac.legacy is False

        assert hvac.current_temperature == 22
        assert hvac.target_temperature == 21
        assert hvac.started_at == ""
        assert hvac.status == ""
        assert hvac.type == ""
        assert hvac.duration == 1
        assert hvac.command_id == ""
        assert isinstance(hvac.options, dict)
        assert hvac.options == {
            "frontDefogger": "",
            "frontDriverSeatHeater": "",
            "frontPassengerSeatHeater": "",
            "mirrorHeater": "",
            "rearDefogger": "",
            "rearDriverSeatHeater": "",
            "rearPassengerSeatHeater": "",
            "steeringHeater": "",
        }

        assert hvac.last_updated == "2020-10-16T03:50:15Z"

        assert hvac.front_defogger_is_on is None
        assert hvac.rear_defogger_is_on is None
        assert hvac.blower_on is None

    def test_hvac_legacy(self):
        """Test legacy Hvac"""
        hvac = self._create_example_legacy_data()

        assert hvac.legacy is True

        assert hvac.current_temperature == 22
        assert hvac.target_temperature == 21
        assert hvac.blower_on == 0
        assert hvac.front_defogger_is_on is False
        assert hvac.rear_defogger_is_on is False
        assert hvac.last_updated is None

        assert hvac.started_at is None
        assert hvac.status is None
        assert hvac.type is None
        assert hvac.duration is None
        assert hvac.options is None
        assert hvac.command_id is None

    def test_hvac_no_data(self):
        """Test Hvac with no initialization data"""
        hvac = Hvac({})

        assert hvac.legacy is False

        assert hvac.current_temperature is None
        assert hvac.target_temperature is None
        assert hvac.started_at is None
        assert hvac.status is None
        assert hvac.type is None
        assert hvac.duration is None
        assert hvac.command_id is None
        assert hvac.options is None

        assert hvac.last_updated is None
