"""Models for vehicle sensors."""
from __future__ import annotations

from mytoyota.models.data import VehicleData


class Door(VehicleData):
    """Door/hood data model."""

    @property
    def warning(self) -> bool | None:
        """If warning exists for the door."""
        return self._data.get("warning")

    @property
    def closed(self) -> bool | None:
        """If the door is closed."""
        return self._data.get("closed")

    @property
    def locked(self) -> bool | None:
        """If the door is locked."""
        return self._data.get("locked")


class Doors(VehicleData):
    """Trunk/doors/hood data model."""

    @property
    def warning(self) -> bool | None:
        """If warning exists for one of the doors."""
        return self._data.get("warning")

    @property
    def driver_seat(self) -> Door:
        """Driver seat door."""
        return Door(self._data.get("driverSeatDoor"))

    @property
    def passenger_seat(self) -> Door:
        """Passenger seat door."""
        return Door(self._data.get("passengerSeatDoor"))

    @property
    def leftrear_seat(self) -> Door:
        """Left rearseat door."""
        return Door(self._data.get("rearLeftSeatDoor"))

    @property
    def rightrear_seat(self) -> Door:
        """Right rearseat door."""
        return Door(self._data.get("rearRightSeatDoor"))

    @property
    def trunk(self) -> Door:
        """Trunk."""
        return Door(self._data.get("backDoor"))


class Window(VehicleData):
    """Window data model."""

    @property
    def warning(self) -> bool | None:
        """If a warning exists for the window."""
        return self._data.get("warning")

    @property
    def state(self) -> str | None:
        """Window state."""
        return self._data.get("state")


class Windows(VehicleData):
    """Windows data model."""

    @property
    def warning(self) -> bool | None:
        """If a warning exists for one of the windows."""
        return self._data.get("warning")

    @property
    def driver_seat(self) -> Window:
        """Driver seat window."""
        return Window(self._data.get("driverSeatWindow"))

    @property
    def passenger_seat(self) -> Window:
        """Passenger seat window."""
        return Window(self._data.get("passengerSeatWindow"))

    @property
    def leftrear_seat(self) -> Window:
        """Left rearseat window."""
        return Window(self._data.get("rearLeftSeatWindow"))

    @property
    def rightrear_seat(self) -> Window:
        """Right rearseat window."""
        return Window(self._data.get("rearRightSeatWindow"))


class Light(VehicleData):
    """Vehicle light data model."""

    @property
    def warning(self) -> bool | None:
        """If a warning exists for the light."""
        return self._data.get("warning")

    @property
    def off(self) -> bool | None:
        """If the light is off."""
        return self._data.get("off")


class Lights(VehicleData):
    """Vehicle lights data model."""

    @property
    def warning(self) -> bool | None:
        """If a warning exists for one of the lights."""
        return self._data.get("warning")

    @property
    def headlights(self) -> Light:
        """Headlights."""
        return Light(self._data.get("headLamp"))

    @property
    def taillights(self) -> Light:
        """Taillights."""
        return Light(self._data.get("tailLamp"))

    @property
    def hazardlights(self) -> Light:
        """Hazardlights."""
        return Light(self._data.get("hazardLamp"))


class Key(VehicleData):
    """Keyfob data model."""

    @property
    def warning(self) -> bool | None:
        """If a warning exists for the key.."""
        return self._data.get("warning")

    @property
    def in_car(self) -> bool | None:
        """If the key is in the car."""
        return self._data.get("inCar")


class Sensors(VehicleData):
    """Vehicle sensors data model."""

    @property
    def overallstatus(self) -> str | None:
        """If a warning exists for any of the sensors."""
        return self._data.get("overallStatus")

    @property
    def last_updated(self) -> str | None:
        """Last time data was recieved from the car."""
        return self._data.get("timestamp")

    @property
    def lights(self) -> Lights:
        """Lights."""
        return Lights(self._data.get("lamps"))

    @property
    def hood(self) -> Door:
        """Hood."""
        return Door(self._data.get("hood"))

    @property
    def doors(self) -> Doors:
        """Doors."""
        return Doors(self._data.get("doors"))

    @property
    def windows(self) -> Windows:
        """Windows."""
        return Windows(self._data.get("windows"))

    @property
    def key(self) -> Key:
        """Key."""
        return Key(self._data.get("key"))
