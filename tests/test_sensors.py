"""pytest tests for mytoyota.sensors"""

from mytoyota.sensors import Door, Hood, Key, Light, Window

# pylint: disable=no-self-use


class TestSensors:
    """pytest functions to test Sensors"""

    def test_hood(self):
        """Test hood"""
        hood = Hood({"warning": False, "closed": True})

        assert hood.warning is False
        assert hood.closed is True

        assert hood.as_dict() == {"warning": False, "closed": True}

    def test_hood_no_data(self):
        """Test hood with no initialization data"""
        hood = Hood({})

        assert hood.warning is None
        assert hood.closed is None

        assert hood.as_dict() == {"warning": None, "closed": None}

    def test_door(self):
        """Test door"""
        door = Door({"warning": False, "closed": True, "locked": False})

        assert door.warning is False
        assert door.closed is True
        assert door.locked is False

        assert door.as_dict() == {"warning": False, "closed": True, "locked": False}

    def test_door_no_data(self):
        """Test door with no initialization data"""
        door = Door({})

        assert door.warning is None
        assert door.closed is None
        assert door.locked is None

        assert door.as_dict() == {"warning": None, "closed": None, "locked": None}

    def test_window(self):
        """Test window"""
        window = Window({"warning": False, "state": "close"})

        assert window.warning is False
        assert window.state == "close"

        assert window.as_dict() == {"warning": False, "state": "close"}

    def test_window_no_data(self):
        """Test window with no initialization data"""
        window = Window({})

        assert window.warning is None
        assert window.state is None

        assert window.as_dict() == {"warning": None, "state": None}

    def test_light(self):
        """Test light"""
        light = Light({"warning": False, "off": True})

        assert light.warning is False
        assert light.off is True

        assert light.as_dict() == {"warning": False, "off": True}

    def test_light_no_data(self):
        """Test light with no initialization data"""
        light = Light({})

        assert light.warning is None
        assert light.off is None

        assert light.as_dict() == {"warning": None, "off": None}

    def test_key(self):
        """Test key"""
        key = Key({"warning": False, "inCar": True})

        assert key.warning is False
        assert key.in_car is True

        assert key.as_dict() == {"warning": False, "in_car": True}

    def test_key_no_data(self):
        """Test key with no initialization data"""
        key = Key({})

        assert key.warning is None
        assert key.in_car is None

        assert key.as_dict() == {"warning": None, "in_car": None}
