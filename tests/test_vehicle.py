"""pytest tests for mytoyota.models.vehicle.Vehicle"""
import json
import os
import os.path

import pytest

from mytoyota.models.dashboard import Dashboard
from mytoyota.models.hvac import Hvac
from mytoyota.models.location import ParkingLocation
from mytoyota.models.sensors import Sensors
from mytoyota.models.vehicle import Vehicle


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
        vehicle = Vehicle({}, {})

        assert vehicle.vehicle_id is None
        assert vehicle.vin is None
        assert vehicle.alias == "My vehicle"
        assert vehicle.hybrid is False
        assert vehicle.fueltype == "Unknown"
        assert vehicle.details is None
        assert vehicle.is_connected_services_enabled is False
        assert vehicle.dashboard is None
        assert vehicle.sensors is None
        assert vehicle.hvac is None
        assert vehicle.parkinglocation is None

    def test_vehicle_init_no_status(self):
        """Test vehicle initialization with no status"""

        data_files = os.path.join(os.path.curdir, "tests", "data")

        vehicle_fixtures = self._load_from_file(
            os.path.join(data_files, "vehicles.json")
        )

        for veh in vehicle_fixtures:
            vehicle = Vehicle(vehicle_info=veh, connected_services={})

            assert vehicle.is_connected_services_enabled is False
            assert vehicle.dashboard is None
            assert vehicle.sensors is None
            assert vehicle.hvac is None
            assert vehicle.parkinglocation is None
            assert vehicle.sensors is None

    @pytest.mark.parametrize(
        "vin,connected_services",
        [
            (None, {}),
            (None, {"connectedService": {"status": "ACTIVE"}}),
            ("VINVIN123VIN", None),
            ("VINVIN123VIN", {}),
            # ("VINVIN123VIN", {"connectedService": None}),
            ("VINVIN123VIN", {"connectedService": {}}),
            ("VINVIN123VIN", {"connectedService": {"status": None}}),
            ("VINVIN123VIN", {"connectedService": {"status": ""}}),
            ("VINVIN123VIN", {"connectedService": {"status": "DISABLED"}}),
            ("VINVIN123VIN", {"connectedService": {"error_status": "ACTIVE"}}),
            ("VINVIN123VIN", {"error_connectedService": {"status": "ACTIVE"}}),
        ],
    )
    def test_vehicle_disabled_connected_services(self, vin, connected_services):
        """Test the check if the connected services is disabled"""
        car = {"vin": vin}
        vehicle = Vehicle(vehicle_info=car, connected_services=connected_services)
        assert vehicle.is_connected_services_enabled is False

    def test_vehicle_init(self):
        """Test vehicle initialization with connected services"""

        data_files = os.path.join(os.path.curdir, "tests", "data")

        vehicle_fixtures = self._load_from_file(
            os.path.join(data_files, "vehicles.json")
        )

        for veh in vehicle_fixtures:
            vehicle = Vehicle(
                vehicle_info=veh,
                connected_services={
                    "connectedService": {
                        "devices": [
                            {
                                "brand": "TOYOTA",
                                "state": "ACTIVE",
                                "vin": veh.get("vin"),
                            }
                        ]
                    }
                },
            )

            assert vehicle.vin == veh.get("vin")
            assert vehicle.alias == veh.get("alias", "My vehicle")
            assert vehicle.vehicle_id == veh.get("id")
            assert vehicle.hybrid == veh.get("hybrid", False)
            assert isinstance(vehicle.fueltype, str)
            assert isinstance(vehicle.details, dict)

            print(vehicle.vehicle_id)

            if vehicle.vin is None:
                assert vehicle.is_connected_services_enabled is False
                assert vehicle.dashboard is None
                assert vehicle.sensors is None
                assert vehicle.hvac is None
                assert vehicle.parkinglocation is None
            else:
                assert vehicle.is_connected_services_enabled is True
                assert vehicle.dashboard is None
                assert vehicle.sensors is None
                assert vehicle.hvac is None
                assert vehicle.parkinglocation is None

    def test_vehicle_init_status(self):
        """Test vehicle initialization with connected services with status"""

        data_files = os.path.join(os.path.curdir, "tests", "data")

        vehicle_fixtures = self._load_from_file(
            os.path.join(data_files, "vehicles.json")
        )
        odometer_fixture = self._load_from_file(
            os.path.join(data_files, "vehicle_JTMW1234565432109_odometer.json")
        )
        status_fixture = self._load_from_file(
            os.path.join(data_files, "vehicle_JTMW1234565432109_status.json")
        )

        vehicle = Vehicle(
            vehicle_info=vehicle_fixtures[0],
            connected_services={
                "connectedService": {
                    "devices": [
                        {
                            "brand": "TOYOTA",
                            "state": "ACTIVE",
                            "vin": vehicle_fixtures[0].get("vin"),
                        }
                    ]
                }
            },
            odometer=odometer_fixture,
            status=status_fixture,
        )

        assert vehicle.fueltype == status_fixture["energy"][0]["type"].capitalize()
        assert isinstance(vehicle.parkinglocation, ParkingLocation)
        assert isinstance(vehicle.sensors, Sensors)
        assert vehicle.hvac is None
        assert isinstance(vehicle.dashboard, Dashboard)
        assert vehicle.dashboard.legacy is False
        assert vehicle.dashboard.fuel_level == status_fixture["energy"][0]["level"]
        assert vehicle.dashboard.is_metric is True
        assert vehicle.dashboard.odometer == odometer_fixture[0]["value"]
        assert (
            vehicle.dashboard.fuel_range
            == status_fixture["energy"][0]["remainingRange"]
        )
        assert vehicle.dashboard.battery_level is None
        assert vehicle.dashboard.battery_range is None
        assert vehicle.dashboard.battery_range_with_aircon is None
        assert vehicle.dashboard.charging_status is None
        assert vehicle.dashboard.remaining_charge_time is None

    def test_vehicle_init_status_legacy(self):
        """Test vehicle initialization with connected services with legacy status"""

        data_files = os.path.join(os.path.curdir, "tests", "data")

        vehicle_fixtures = self._load_from_file(
            os.path.join(data_files, "vehicles.json")
        )
        odometer_fixture = self._load_from_file(
            os.path.join(data_files, "vehicle_JTMW1234565432109_odometer_legacy.json")
        )
        status_fixture = self._load_from_file(
            os.path.join(data_files, "vehicle_JTMW1234565432109_status_legacy.json")
        )

        vehicle = Vehicle(
            vehicle_info=vehicle_fixtures[0],
            connected_services={
                "connectedService": {
                    "devices": [
                        {
                            "brand": "TOYOTA",
                            "state": "ACTIVE",
                            "vin": vehicle_fixtures[0].get("vin"),
                        }
                    ]
                }
            },
            odometer=odometer_fixture,
            status_legacy=status_fixture,
        )

        assert vehicle.fueltype == "Petrol"
        assert vehicle.parkinglocation is None
        assert vehicle.sensors is None
        assert isinstance(vehicle.hvac, Hvac)
        assert isinstance(vehicle.dashboard, Dashboard)
        assert vehicle.dashboard.legacy is True
        assert vehicle.dashboard.fuel_level == odometer_fixture[1]["value"]
        assert vehicle.dashboard.is_metric is True
        assert vehicle.dashboard.odometer == odometer_fixture[0]["value"]
        assert (
            vehicle.dashboard.fuel_range
            == status_fixture["VehicleInfo"]["ChargeInfo"]["GasolineTravelableDistance"]
        )
        assert (
            vehicle.dashboard.battery_level
            == status_fixture["VehicleInfo"]["ChargeInfo"]["ChargeRemainingAmount"]
        )
        assert (
            vehicle.dashboard.battery_range
            == status_fixture["VehicleInfo"]["ChargeInfo"]["EvDistanceInKm"]
        )
        assert (
            vehicle.dashboard.battery_range_with_aircon
            == status_fixture["VehicleInfo"]["ChargeInfo"]["EvDistanceWithAirCoInKm"]
        )
        assert (
            vehicle.dashboard.charging_status
            == status_fixture["VehicleInfo"]["ChargeInfo"]["ChargingStatus"]
        )
        assert (
            vehicle.dashboard.remaining_charge_time
            == status_fixture["VehicleInfo"]["ChargeInfo"]["RemainingChargeTime"]
        )
