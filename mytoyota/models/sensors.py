"""Models for vehicle sensors."""
from __future__ import annotations
from mytoyota.models.data import VehicleData


class Door(VehicleData):
    """Door/hood data model."""

    @property
    def warning(self) -> bool | None:
        return self._data.get("warning")
    
    @property
    def closed(self) -> bool | None:
        return self._data.get("closed")
    
    @property
    def locked(self) -> bool | None:
        return self._data.get("locked")

class Doors(VehicleData):
    """Trunk/doors/hood data model."""

    @property
    def warning(self) -> bool | None:
        return self._data.get("warning")

    @property
    def driver_seat(self) -> Door:
        return Door(self._data.get("driverSeatDoor"))
    
    @property
    def passenger_seat(self) -> Door:
        return Door(self._data.get("passengerSeatDoor"))
    
    @property
    def leftrear_seat(self) -> Door:
        return Door(self._data.get("rearLeftSeatDoor"))
    
    @property
    def rightrear_seat(self) -> Door:
        return Door(self._data.get("rearRightSeatDoor"))
    
    @property
    def trunk(self) -> Door:
        return Door(self._data.get("backDoor"))

class Window(VehicleData):
    """Window data model."""

    @property
    def warning(self) -> bool | None:
        return self._data.get("warning")
    
    @property
    def state(self) -> str | None:
        return self._data.get("state")

class Windows(VehicleData):
    """Windows data model."""

    @property
    def warning(self) -> bool | None:
        return self._data.get("warning")

    @property
    def driver_seat(self) -> Window:
        return Window(self._data.get("driverSeatWindow"))
    
    @property
    def passenger_seat(self) -> Window:
        return Window(self._data.get("passengerSeatWindow"))
    
    @property
    def leftrear_seat(self) -> Window:
        return Window(self._data.get("rearLeftSeatWindow"))
    
    @property
    def rightrear_seat(self) -> Window:
        return Window(self._data.get("rearRightSeatWindow"))

class Light(VehicleData):
    """Vehicle light data model."""

    @property
    def warning(self) -> bool | None:
        return self._data.get("warning")

    @property
    def off(self) -> bool | None:
        return self._data.get("off")

class Lights(VehicleData):
    """Vehicle lights data model."""

    @property
    def warning(self) -> bool | None:
        return self._data.get("warning")

    @property
    def headlights(self) -> Light:
        return Light(self._data.get("headLamp"))
    
    @property
    def taillights(self) -> Light:
        return Light(self._data.get("tailLamp"))
    
    @property
    def hazardlights(self) -> Light:
        return Light(self._data.get("hazardLamp"))

class Key(VehicleData):
    """Keyfob data model."""

    @property
    def warning(self) -> bool | None:
        return self._data.get("warning")
    
    @property
    def in_car(self) -> bool | None:
        return self._data.get("inCar")


class Sensors(VehicleData):
    """Vehicle sensors data model."""

    @property
    def overallstatus(self) -> str | None:
        return self._data.get("overallStatus")
    
    @property
    def last_updated(self) -> str | None:
        return self._data.get("timestamp")
    
    @property
    def lights(self) -> Lights:
        return Lights(self._data.get("lamps"))
    
    @property
    def hood(self) -> Door:
        return Door(self._data.get("hood"))
    
    @property
    def doors(self) -> Doors:
        return Doors(self._data.get("doors"))
    
    @property
    def windows(self) -> Windows:
        return Windows(self._data.get("windows"))
    
    @property
    def key(self) -> Key:
        return Key(self._data.get("key"))
    
