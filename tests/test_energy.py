"""pytest tests for mytoyota.status.Energy"""

from mytoyota.status import Energy

# pylint: disable=no-self-use


class TestEnergy:
    """pytest functions to test Energy"""

    @staticmethod
    def _create_example_data():
        """Create list with predefined data"""
        return [
            {
                "timestamp": "2021-09-19T14:02:37Z",
                "type": "HYDROGEN",
                "level": 58.8,
                "remainingRange": 295,
            }
        ]

    @staticmethod
    def _create_example_legacy_data():
        """Create dict with predefined data"""
        return {"Fuel": 69}

    @staticmethod
    def _create_example_battery_data():
        """Create dict with predefined data"""
        return {
            "BatteryPowerSupplyPossibleTime": 16383,
            "ChargeEndTime": "00:00",
            "ChargeRemainingAmount": 100,
            "ChargeStartTime": "22:10",
            "ChargeType": 1,
            "ChargeWeek": 5,
            "ChargingStatus": "chargeComplete",
            "ConnectorStatus": 5,
            "EvDistanceInKm": 79.9,
            "EvDistanceWithAirCoInKm": 73.51,
            "EvTravelableDistance": 79.9,
            "EvTravelableDistanceSubtractionRate": 8,
            "PlugInHistory": 33,
            "PlugStatus": 45,
            "RemainingChargeTime": 65535,
            "SettingChangeAcceptanceStatus": 0,
        }

    def test_energy_km(self):
        """Test energy in unit km"""
        energy = Energy(self._create_example_data())

        assert energy.level == 58.8
        assert energy.range == 295
        assert energy.type == "Hydrogen"
        assert energy.last_updated == "2021-09-19T14:02:37Z"

    def test_energy_mi(self):
        """Test energy in unit mi"""
        energy = Energy(self._create_example_data(), unit="mi")

        assert energy.legacy is False

        assert energy.level == 58.8
        assert energy.range == 183.3045
        assert energy.type == "Hydrogen"
        assert energy.last_updated == "2021-09-19T14:02:37Z"

    def test_energy_no_data(self):
        """Test energy in unit mi"""
        energy = Energy([{}])

        assert energy.legacy is False

        assert energy.level is None
        assert energy.range is None
        assert energy.type == "Unknown"
        assert energy.last_updated is None

    def test_energy_str(self):
        """Test energy converted to string"""
        energy = Energy(self._create_example_data())

        string = str(energy)
        assert isinstance(string, str)
        assert (
            string == "{'level': 58.8, 'range': 295, 'type': 'Hydrogen', "
            "'last_updated': '2021-09-19T14:02:37Z'}"
        )

    def test_energy_dict(self):
        """Test energy converted to dict"""
        energy = Energy(self._create_example_data())

        dictionary = energy.as_dict()
        assert isinstance(dictionary, dict)
        assert dictionary == {
            "level": 58.8,
            "range": 295,
            "type": "Hydrogen",
            "last_updated": "2021-09-19T14:02:37Z",
        }

    def test_energy_legacy_km(self):
        """Test legacy energy in unit km"""
        energy = Energy(self._create_example_legacy_data(), legacy=True)

        assert energy.legacy is True
        assert energy.level == 69

        energy.type = "Petrol"

        assert energy.type == "Petrol"
        assert energy.chargeinfo is None

        energy.set_battery_attributes(self._create_example_battery_data())

        assert energy.range == 79.9
        assert energy.range_with_aircon == 73.51
        assert isinstance(energy.chargeinfo, dict)
        assert energy.chargeinfo == {
            "status": "chargeComplete",
            "remaining_time": 65535,
            "remaining_amount": 100,
            "start_time": "22:10",
            "end_time": "00:00",
        }

    def test_energy_legacy_mi(self):
        """Test legacy energy in unit km"""
        energy = Energy(self._create_example_legacy_data(), unit="mi", legacy=True)

        assert energy.legacy is True
        assert energy.level == 69

        energy.type = "Petrol"

        assert energy.type == "Petrol"
        assert energy.chargeinfo is None

        energy.set_battery_attributes(self._create_example_battery_data())

        assert energy.range == 49.6476
        assert energy.range_with_aircon == 45.677
        assert isinstance(energy.chargeinfo, dict)
        assert energy.chargeinfo == {
            "status": "chargeComplete",
            "remaining_time": 65535,
            "remaining_amount": 100,
            "start_time": "22:10",
            "end_time": "00:00",
        }

    def test_energy_legacy_no_data(self):
        """Test energy in unit mi"""
        energy = Energy({}, legacy=True)

        assert energy.legacy is True
        assert energy.level is None

        assert energy.type is None
        assert energy.chargeinfo is None

        energy.set_battery_attributes({})

        assert energy.range is None
        assert energy.range_with_aircon is None
        assert isinstance(energy.chargeinfo, dict)
        assert energy.chargeinfo == {
            "status": None,
            "remaining_time": None,
            "remaining_amount": None,
            "start_time": None,
            "end_time": None,
        }

    def test_energy_legacy_str(self):
        """Test energy converted to string"""
        energy = Energy(self._create_example_legacy_data(), legacy=True)

        string = str(energy)
        assert isinstance(string, str)
        assert string == "{'legacy': True, 'level': 69}"

        energy.type = "Petrol"

        energy.set_battery_attributes(self._create_example_battery_data())

        string_with_battery = str(energy)
        assert isinstance(string_with_battery, str)
        assert (
            string_with_battery
            == "{'legacy': True, 'level': 69, 'type': 'Petrol', 'range': 79.9, "
            "'range_with_aircon': 73.51, "
            "'chargeinfo': {'status': 'chargeComplete', 'remaining_time': 65535, "
            "'remaining_amount': 100, "
            "'start_time': '22:10', 'end_time': '00:00'}}"
        )

    def test_energy_legacy_dict(self):
        """Test energy converted to dict"""
        energy = Energy(self._create_example_legacy_data(), legacy=True)

        dictionary = energy.as_dict()
        assert isinstance(dictionary, dict)
        assert dictionary == {
            "level": 69,
            "legacy": True,
        }

        energy.type = "Petrol"

        energy.set_battery_attributes(self._create_example_battery_data())

        dict_with_battery = energy.as_dict()
        assert isinstance(dict_with_battery, dict)
        assert dict_with_battery == {
            "level": 69,
            "legacy": True,
            "type": "Petrol",
            "range": 79.9,
            "range_with_aircon": 73.51,
            "chargeinfo": {
                "status": "chargeComplete",
                "remaining_time": 65535,
                "remaining_amount": 100,
                "start_time": "22:10",
                "end_time": "00:00",
            },
        }
