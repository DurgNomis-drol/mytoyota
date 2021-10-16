"""Sensor representation for mytoyota"""
from typing import Optional

from mytoyota.const import CLOSED, INCAR, LOCKED, OFF, STATE, WARNING


class Hood:
    """Representation of the hood of the car"""

    def __init__(self, hood: dict) -> None:
        self.warning: Optional[bool] = hood.get(WARNING, None)
        self.closed: Optional[bool] = hood.get(CLOSED, None)

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return vars(self)


class Door:
    """Representation of a door"""

    def __init__(self, door: dict) -> None:
        self.warning: Optional[bool] = door.get(WARNING, None)
        self.closed: Optional[bool] = door.get(CLOSED, None)
        self.locked: Optional[bool] = door.get(LOCKED, None)

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
        self.warning = doors.get(WARNING, None)

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

    def __init__(self, window) -> None:
        self.warning: Optional[bool] = window.get(WARNING, None)
        self.state: Optional[str] = window.get(STATE, None)

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
        self.warning = windows.get(WARNING, None)

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

    def __init__(self, light: dict) -> None:
        self.warning: Optional[bool] = light.get(WARNING, None)
        self.off: Optional[bool] = light.get(OFF, None)

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

    def __init__(self, key: dict) -> None:
        self.warning: Optional[bool] = key.get(WARNING, None)
        self.in_car: Optional[bool] = key.get(INCAR, None)

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return vars(self)
