"""pytest tests for mytoyota.models.sensors"""
import json
import os
import os.path

from mytoyota.models.sensors import (
    Door,
    Doors,
    Key,
    Light,
    Lights,
    Sensors,
    Window,
    Windows,
)


class TestSensors:  # pylint: disable=too-many-public-methods
    """pytest functions to test Sensors"""

    @staticmethod
    def _load_from_file(filename: str):
        """Load a data structure from the specified JSON filename, and
        return it."""
        with open(filename, encoding="UTF-8") as json_file:
            return json.load(json_file)

    def test_hood(self):
        """Test hood"""
        hood = Door({"warning": False, "closed": True})

        assert hood.warning is False
        assert hood.closed is True
        assert hood.locked is None

    def test_hood_no_data(self):
        """Test hood with no initialization data"""
        hood = Door({})

        assert hood.warning is None
        assert hood.closed is None
        assert hood.locked is None

    @staticmethod
    def _create_example_door():
        """Create a door with predefined data"""
        return Door({"warning": False, "closed": True, "locked": False})

    def test_door(self):
        """Test door"""
        door = self._create_example_door()

        assert door.warning is False
        assert door.closed is True
        assert door.locked is False

    def test_door_no_data(self):
        """Test door with no initialization data"""
        door = Door({})

        assert door.warning is None
        assert door.closed is None
        assert door.locked is None

    def test_doors(self):
        """Test Doors"""
        doors = {
            "warning": False,
            "driverSeatDoor": {"warning": False, "closed": True, "locked": False},
            "passengerSeatDoor": {"warning": False, "closed": True, "locked": False},
            "rearRightSeatDoor": {"warning": False, "closed": True, "locked": False},
            "rearLeftSeatDoor": {"warning": False, "closed": True, "locked": False},
            "backDoor": {"warning": False, "closed": True, "locked": False},
        }

        doors = Doors(doors)

        assert doors.warning is False
        assert isinstance(doors.driver_seat, Door)
        assert isinstance(doors.passenger_seat, Door)
        assert isinstance(doors.leftrear_seat, Door)
        assert isinstance(doors.rightrear_seat, Door)
        assert isinstance(doors.trunk, Door)

    def test_doors_no_data(self):
        """Test Windows with no initialization data"""
        doors = Doors({})

        assert doors.warning is None
        assert isinstance(doors.driver_seat, Door)
        assert isinstance(doors.passenger_seat, Door)
        assert isinstance(doors.leftrear_seat, Door)
        assert isinstance(doors.rightrear_seat, Door)
        assert isinstance(doors.trunk, Door)

    @staticmethod
    def _create_example_window():
        """Create a window with predefined data"""
        return Window({"warning": False, "state": "close"})

    def test_window(self):
        """Test window"""
        window = self._create_example_window()

        assert window.warning is False
        assert window.state == "close"

    def test_window_no_data(self):
        """Test window with no initialization data"""
        window = Window({})

        assert window.warning is None
        assert window.state is None

    def test_windows(self):
        """Test Windows"""
        windows = {
            "warning": False,
            "driverSeatWindow": {"warning": False, "state": "close"},
            "passengerSeatWindow": {"warning": False, "state": "close"},
            "rearRightSeatWindow": {"warning": False, "state": "close"},
            "rearLeftSeatWindow": {"warning": False, "state": "close"},
        }

        windows = Windows(windows)

        assert windows.warning is False
        assert isinstance(windows.driver_seat, Window)
        assert isinstance(windows.passenger_seat, Window)
        assert isinstance(windows.rightrear_seat, Window)
        assert isinstance(windows.leftrear_seat, Window)

    def test_windows_no_data(self):
        """Test Windows with no initialization data"""
        windows = Windows({})

        assert windows.warning is None
        assert isinstance(windows.driver_seat, Window)
        assert isinstance(windows.passenger_seat, Window)
        assert isinstance(windows.rightrear_seat, Window)
        assert isinstance(windows.leftrear_seat, Window)

    @staticmethod
    def _create_example_light():
        """Create a example light with predefined data."""
        return Light({"warning": False, "off": True})

    def test_light(self):
        """Test light"""
        light = self._create_example_light()

        assert light.warning is False
        assert light.off is True

    def test_light_no_data(self):
        """Test light with no initialization data"""
        light = Light({})

        assert light.warning is None
        assert light.off is None

    def test_lights(self):
        """Test ligts"""
        lights = {
            "warning": False,
            "headLamp": {"warning": False, "off": True},
            "tailLamp": {"warning": False, "off": True},
            "hazardLamp": {"warning": False, "off": True},
        }

        lights = Lights(lights)

        assert lights.warning is False
        assert isinstance(lights.headlights, Light)
        assert isinstance(lights.taillights, Light)
        assert isinstance(lights.hazardlights, Light)

    def test_lights_no_data(self):
        """Test Lights with no initialization data"""
        lights = Lights({})

        assert lights.warning is None
        assert isinstance(lights.headlights, Light)
        assert isinstance(lights.taillights, Light)
        assert isinstance(lights.hazardlights, Light)

    def test_key(self):
        """Test key"""
        key = Key({"warning": False, "inCar": True})

        assert key.warning is False
        assert key.in_car is True

    def test_key_no_data(self):
        """Test key with no initialization data"""
        key = Key({})

        assert key.warning is None
        assert key.in_car is None

    def test_sensors(self):
        """Test sensors"""
        data_files = os.path.join(os.path.curdir, "tests", "data")
        fixture = self._load_from_file(os.path.join(data_files, "vehicle_JTMW1234565432109_status.json"))
        sensors = Sensors(fixture.get("protectionState"))

        assert sensors.overallstatus == "OK"
        assert sensors.last_updated == "2021-10-12T15:22:53Z"
        assert isinstance(sensors.doors, Doors)
        assert sensors.doors.driver_seat.warning is False
        assert sensors.doors.driver_seat.closed is True
        assert sensors.doors.driver_seat.locked is True
        assert isinstance(sensors.hood, Door)
        assert sensors.hood.warning is False
        assert sensors.hood.closed is True
        assert sensors.hood.locked is None
        assert isinstance(sensors.lights, Lights)
        assert sensors.lights.headlights.warning is False
        assert sensors.lights.headlights.off is True
        assert isinstance(sensors.windows, Windows)
        assert sensors.windows.passenger_seat.warning is False
        assert sensors.windows.passenger_seat.state == "close"
        assert isinstance(sensors.key, Key)

        assert isinstance(sensors.raw_json, dict)
        assert sensors.raw_json == fixture.get("protectionState")
