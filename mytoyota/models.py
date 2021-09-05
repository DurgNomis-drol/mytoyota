"""Models for mytoyota"""

from mytoyota.const import CLOSED, HOOD, INCAR, LOCKED, OFF, STATE, WARNING


class Hood:
    """Representation of the hood of the car"""

    warning: bool = False
    closed: bool = True

    def __init__(self, hood):
        self.warning = hood[WARNING]
        self.closed = hood[CLOSED]

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

    def __init__(self, door) -> None:
        self.warning = door[WARNING]
        self.closed = door[CLOSED]
        self.locked = door[LOCKED]

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

    hood: Hood
    driverseat: Door
    passengerseat: Door
    rightrearseat: Door
    leftrearseat: Door
    tailgate: Door
    warning: bool = False

    def __init__(self, hood, doors):
        self.warning = doors[WARNING]

        self.hood = Hood(hood)
        self.driverseat = (
            Door(doors["driverSeatDoor"]) if "driverSeatDoor" in doors else None
        )
        self.passengerseat = (
            Door(doors["passengerSeatDoor"]) if "passengerSeatDoor" in doors else None
        )
        self.rightrearseat = (
            Door(doors["rearRightSeatDoor"]) if "rearRightSeatDoor" in doors else None
        )
        self.leftrearseat = (
            Door(doors["rearLeftSeatDoor"]) if "rearLeftSeatDoor" in doors else None
        )
        self.tailgate = Door(doors["backDoor"]) if "backDoor" in doors else None

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return {
            WARNING: self.warning,
            HOOD: self.hood.as_dict(),
            "driverseat": self.driverseat.as_dict(),
            "passengerseat": self.passengerseat.as_dict(),
            "rightrearseat": self.rightrearseat.as_dict(),
            "leftrearseat": self.rightrearseat.as_dict(),
            "tailgate": self.tailgate.as_dict(),
        }


class Window:
    """Representation of a window"""

    warning: bool = False
    state: str = None

    def __init__(self, window) -> None:
        self.warning = window[WARNING]
        self.state = window[STATE]

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

    def __init__(self, windows):
        self.warning = windows[WARNING]

        self.driverseat = (
            Window(windows["driverSeatWindow"])
            if "driverSeatWindow" in windows
            else None
        )
        self.passengerseat = (
            Window(windows["passengerSeatWindow"])
            if "passengerSeatWindow" in windows
            else None
        )
        self.rightrearseat = (
            Window(windows["rearRightSeatWindow"])
            if "rearRightSeatWindow" in windows
            else None
        )
        self.leftrearseat = (
            Window(windows["rearLeftSeatWindow"])
            if "rearLeftSeatWindow" in windows
            else None
        )

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

    def __init__(self, light):
        self.warning = light[WARNING]
        self.off = light[OFF]

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

    def __init__(self, lights):
        self.warning = lights[WARNING]

        self.front = Light(lights["headLamp"]) if "headLamp" in lights else None
        self.back = Light(lights["tailLamp"]) if "tailLamp" in lights else None
        self.hazard = Light(lights["hazardLamp"]) if "hazardLamp" in lights else None

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

    def __init__(self, key):
        self.warning = key[WARNING]
        self.in_car = key[INCAR]

    def __str__(self) -> str:
        return str(self.as_dict())

    def as_dict(self) -> dict:
        """Return as dict."""
        return vars(self)
