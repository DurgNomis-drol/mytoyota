"""pytest tests for mytoyota.vehicle.Vehicle"""
import json
import os

from mytoyota.vehicle import Vehicle

# pylint: disable=no-self-use


class TestVehicle:
    """pytest functions for Vehicle object"""

    @staticmethod
    def _load_from_file(filename: str):
        """Load a data structure from the specified JSON filename, and
        return it."""
        with open(filename, encoding="UTF-8") as json_file:
            return json.load(json_file)

    def test_vehicle_no_data(self):
        """Test vehicle with no initialization data"""
        vehicle = Vehicle({})

        assert hasattr(vehicle, "id") is False
        assert hasattr(vehicle, "vin") is False
        assert hasattr(vehicle, "alias") is False
        assert vehicle.details is None
        assert vehicle.is_connected is False
        assert vehicle.odometer is None
        assert vehicle.energy is None
        assert vehicle.hvac is None
        assert vehicle.parking is None

    def test_vehicle_init_no_status(self):
        """Test vehicle initialization with no status"""

        data_files = os.path.join(os.path.curdir, "tests", "data")

        fixtures = self._load_from_file(os.path.join(data_files, "vehicles.json"))

        for veh in fixtures:
            vehicle = Vehicle(vehicle_info=veh)

            assert vehicle.vin == veh.get("vin")
            assert vehicle.is_connected is False
            assert vehicle.odometer is None
            assert vehicle.energy is None
            assert vehicle.hvac is None
            assert vehicle.parking is None

    def test_vehicle_init(self):
        """Test vehicle initialization with connected services"""

        data_files = os.path.join(os.path.curdir, "tests", "data")

        fixtures = self._load_from_file(os.path.join(data_files, "vehicles.json"))

        for veh in fixtures:
            vehicle = Vehicle(
                vehicle_info=veh,
                connected_services={"connectedService": {"status": "ACTIVE"}},
            )

            assert vehicle.vin == veh.get("vin")
            assert vehicle.alias == veh.get("alias")

            print(vehicle.id)

            if vehicle.vin is None:
                assert vehicle.is_connected is False
                assert vehicle.odometer is None
                assert vehicle.energy is None
                assert vehicle.hvac is None
                assert vehicle.parking is None
                assert vehicle.sensors is None
            else:
                assert vehicle.is_connected is True
                assert vehicle.odometer is not None
                assert vehicle.energy is None
                assert vehicle.hvac is None
                assert vehicle.parking is None
                assert vehicle.sensors is None
