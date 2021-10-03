"""Sensor representation for mytoyota"""
import logging

from mytoyota.const import CLOSED, INCAR, LOCKED, OFF, STATE, WARNING

_LOGGER: logging.Logger = logging.getLogger(__package__)


class Hood:
    """Representation of the hood of the car"""

    warning: bool = False
    closed: bool = True

    def __init__(self, hood: dict) -> None:
        self.warning = hood.get(WARNING, None)
        self.closed = hood.get(CLOSED, None)

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return vars(self)


class Door:
    """Representation of a door"""

    warning: bool = False
    closed: bool = True
    locked: bool = True

    def __init__(self, door: dict) -> None:
        self.warning = door.get(WARNING, None)
        self.closed = door.get(CLOSED, None)
        self.locked = door.get(LOCKED, None)

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return {
            WARNING: self.warning,
            CLOSED: self.closed,
            LOCKED: self.locked,
        }


class Doors:
    """Represent all car doors"""

    driverseat: Door
    passengerseat: Door
    rightrearseat: Door
    leftrearseat: Door
    trunk: Door
    warning: bool = False

    def __init__(self, doors: dict):
        self.warning = doors[WARNING]

        self.driverseat = Door(doors.get("driverSeatDoor", {}))
        self.passengerseat = Door(doors.get("passengerSeatDoor", {}))
        self.rightrearseat = Door(doors.get("rearRightSeatDoor", {}))
        self.leftrearseat = Door(doors.get("rearLeftSeatDoor", {}))
        self.trunk = Door(doors.get("backDoor", {}))

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return {
            WARNING: self.warning,
            "driverseat": self.driverseat.as_dict(),
            "passengerseat": self.passengerseat.as_dict(),
            "rightrearseat": self.rightrearseat.as_dict(),
            "leftrearseat": self.rightrearseat.as_dict(),
            "trunk": self.trunk.as_dict(),
        }


class Window:
    """Representation of a window"""

    warning: bool = False
    state: str = None

    def __init__(self, window) -> None:
        self.warning = window.get(WARNING, None)
        self.state = window.get(STATE, None)

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return {
            WARNING: self.warning,
            STATE: self.state,
        }


class Windows:
    """Represent all car windows"""

    driverseat: Window
    passengerseat: Window
    rightrearseat: Window
    leftrearseat: Window

    warning: bool = False

    def __init__(self, windows: dict) -> None:
        self.warning = windows[WARNING]

        self.driverseat = Window(windows.get("driverSeatWindow", {}))
        self.passengerseat = Window(windows.get("passengerSeatWindow", {}))
        self.rightrearseat = Window(windows.get("rearRightSeatWindow", {}))
        self.leftrearseat = Window(windows.get("rearLeftSeatWindow", {}))

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return {
            WARNING: self.warning,
            "driverseat": self.driverseat.as_dict(),
            "passengerseat": self.passengerseat.as_dict(),
            "rightrearseat": self.rightrearseat.as_dict(),
            "leftrearseat": self.rightrearseat.as_dict(),
        }


class Light:
    """Representation of the lights"""

    warning: bool = False
    off: bool = True

    def __init__(self, light: dict) -> None:
        self.warning = light.get(WARNING, None)
        self.off = light.get(OFF, None)

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return {
            WARNING: self.warning,
            OFF: self.off,
        }


class Lights:
    """Represent all car windows"""

    front: Light
    back: Light
    hazard: Light
    warning: bool = False

    def __init__(self, lights: dict) -> None:
        self.warning = lights.get(WARNING, None)

        self.front = Light(lights.get("headLamp", {}))
        self.back = Light(lights.get("tailLamp", {}))
        self.hazard = Light(lights.get("hazardLamp", {}))

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return {
            "warning": self.warning,
            "front": self.front.as_dict(),
            "back": self.back.as_dict(),
            "hazard": self.back.as_dict(),
        }


class Key:
    """Representation of the ignition"""

    warning: bool = False
    in_car: bool = False

    def __init__(self, key: dict) -> None:
        self.warning = key.get(WARNING, None)
        self.in_car = key.get(INCAR, None)

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return vars(self)
