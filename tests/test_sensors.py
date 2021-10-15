"""pytest tests for mytoyota.sensors"""

from mytoyota.sensors import Door, Doors, Hood, Key, Light, Lights, Window, Windows

# pylint: disable=no-self-use


class TestSensors:  # pylint: disable=too-many-public-methods
    """pytest functions to test Sensors"""

    def test_hood(self):
        """Test hood"""
        hood = Hood({"warning": False, "closed": True})

        assert hood.warning is False
        assert hood.closed is True

    def test_hood_no_data(self):
        """Test hood with no initialization data"""
        hood = Hood({})

        assert hood.warning is None
        assert hood.closed is None

    def test_hood_str(self):
        """Test hood converted to str"""
        hood = Hood({"warning": False, "closed": True})

        string = str(hood)
        assert isinstance(string, str)
        assert string == "{'warning': False, 'closed': True}"

    def test_hood_dict(self):
        """Test hood converted to a dictionary"""
        hood = Hood({"warning": False, "closed": True})

        dictionary = hood.as_dict()
        assert isinstance(dictionary, dict)
        assert dictionary == {"warning": False, "closed": True}

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

    def test_door_str(self):
        """Test door converted to str"""
        door = self._create_example_door()

        string = str(door)
        assert isinstance(string, str)
        assert string == "{'warning': False, 'closed': True, 'locked': False}"

    def test_door_dict(self):
        """Test door converted to a dictionary"""
        door = self._create_example_door()

        dictionary = door.as_dict()
        assert isinstance(dictionary, dict)
        assert dictionary == {"warning": False, "closed": True, "locked": False}

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
        assert isinstance(doors.driverseat, Door)
        assert isinstance(doors.passengerseat, Door)
        assert isinstance(doors.rightrearseat, Door)
        assert isinstance(doors.leftrearseat, Door)
        assert isinstance(doors.trunk, Door)

        string = str(doors)
        assert isinstance(string, str)
        assert (
            string == "{'warning': False, "
            "'driverseat': {'warning': False, 'closed': True, 'locked': False}, "
            "'passengerseat': {'warning': False, 'closed': True, 'locked': False}, "
            "'rightrearseat': {'warning': False, 'closed': True, 'locked': False}, "
            "'leftrearseat': {'warning': False, 'closed': True, 'locked': False}, "
            "'trunk': {'warning': False, 'closed': True, "
            "'locked': False}}"
        )

        dictionary = doors.as_dict()
        assert isinstance(dictionary, dict)
        assert dictionary == {
            "warning": False,
            "driverseat": {"warning": False, "closed": True, "locked": False},
            "passengerseat": {"warning": False, "closed": True, "locked": False},
            "rightrearseat": {"warning": False, "closed": True, "locked": False},
            "leftrearseat": {"warning": False, "closed": True, "locked": False},
            "trunk": {"warning": False, "closed": True, "locked": False},
        }

    def test_doors_no_data(self):
        """Test Windows with no initialization data"""
        doors = Doors({})

        assert doors.warning is None
        assert isinstance(doors.driverseat, Door)
        assert isinstance(doors.passengerseat, Door)
        assert isinstance(doors.rightrearseat, Door)
        assert isinstance(doors.leftrearseat, Door)
        assert isinstance(doors.trunk, Door)

        dictionary = doors.as_dict()

        assert isinstance(dictionary, dict)
        assert dictionary == {
            "warning": None,
            "driverseat": {"warning": None, "closed": None, "locked": None},
            "passengerseat": {"warning": None, "closed": None, "locked": None},
            "rightrearseat": {"warning": None, "closed": None, "locked": None},
            "leftrearseat": {"warning": None, "closed": None, "locked": None},
            "trunk": {"warning": None, "closed": None, "locked": None},
        }

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

    def test_window_str(self):
        """Test window converted to str"""
        window = self._create_example_window()

        string = str(window)
        assert isinstance(string, str)
        assert string == "{'warning': False, 'state': 'close'}"

    def test_window_dict(self):
        """Test window converted to a dictionary"""
        window = self._create_example_window()

        dictionary = window.as_dict()
        assert isinstance(dictionary, dict)
        assert dictionary == {"warning": False, "state": "close"}

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
        assert isinstance(windows.driverseat, Window)
        assert isinstance(windows.passengerseat, Window)
        assert isinstance(windows.rightrearseat, Window)
        assert isinstance(windows.leftrearseat, Window)

        string = str(windows)
        assert isinstance(string, str)
        assert (
            string
            == "{'warning': False, 'driverseat': {'warning': False, 'state': 'close'}, "
            "'passengerseat': {'warning': False, 'state': 'close'}, "
            "'rightrearseat': {'warning': False, 'state': 'close'}, "
            "'leftrearseat': {'warning': False, 'state': 'close'}}"
        )

        dictionary = windows.as_dict()
        assert isinstance(dictionary, dict)
        assert dictionary == {
            "warning": False,
            "driverseat": {"warning": False, "state": "close"},
            "passengerseat": {"warning": False, "state": "close"},
            "rightrearseat": {"warning": False, "state": "close"},
            "leftrearseat": {"warning": False, "state": "close"},
        }

    def test_windows_no_data(self):
        """Test Windows with no initialization data"""
        windows = Windows({})

        assert windows.warning is None
        assert isinstance(windows.driverseat, Window)
        assert isinstance(windows.passengerseat, Window)
        assert isinstance(windows.rightrearseat, Window)
        assert isinstance(windows.leftrearseat, Window)

        dictionary = windows.as_dict()

        assert isinstance(dictionary, dict)
        assert dictionary == {
            "warning": None,
            "driverseat": {"warning": None, "state": None},
            "passengerseat": {"warning": None, "state": None},
            "rightrearseat": {"warning": None, "state": None},
            "leftrearseat": {"warning": None, "state": None},
        }

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

    def test_light_str(self):
        """Test light converted to str"""
        light = self._create_example_light()

        string = str(light)
        assert isinstance(string, str)
        assert string == "{'warning': False, 'off': True}"

    def test_light_dict(self):
        """Test light converted to a dictionary"""
        light = self._create_example_light()

        dictionary = light.as_dict()
        assert isinstance(dictionary, dict)
        assert dictionary == {"warning": False, "off": True}

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
        assert isinstance(lights.front, Light)
        assert isinstance(lights.back, Light)
        assert isinstance(lights.hazard, Light)

        string = str(lights)
        assert isinstance(string, str)
        assert (
            string == "{'warning': False, "
            "'front': {'warning': False, 'off': True}, "
            "'back': {'warning': False, 'off': True}, "
            "'hazard': {'warning': False, 'off': True}}"
        )

        dictionary = lights.as_dict()
        assert isinstance(dictionary, dict)
        assert dictionary == {
            "warning": False,
            "front": {"warning": False, "off": True},
            "back": {"warning": False, "off": True},
            "hazard": {"warning": False, "off": True},
        }

    def test_lights_no_data(self):
        """Test Lights with no initialization data"""
        lights = Lights({})

        assert lights.warning is None
        assert isinstance(lights.front, Light)
        assert isinstance(lights.back, Light)
        assert isinstance(lights.hazard, Light)

        dictionary = lights.as_dict()

        assert isinstance(dictionary, dict)
        assert dictionary == {
            "warning": None,
            "front": {"warning": None, "off": None},
            "back": {"warning": None, "off": None},
            "hazard": {"warning": None, "off": None},
        }

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

    def test_key_str(self):
        """Test key converted to str"""
        key = Key({"warning": False, "inCar": True})

        string = str(key)
        assert isinstance(string, str)
        assert string == "{'warning': False, 'in_car': True}"

    def test_key_dict(self):
        """Test key converted to a dictionary"""
        key = Key({"warning": False, "inCar": True})

        dictionary = key.as_dict()
        assert isinstance(dictionary, dict)
        assert dictionary == {"warning": False, "in_car": True}
