"""Models for vehicle sensors."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from mytoyota.models.endpoints.status import (
    RemoteStatusModel,
    RemoteStatusResponseModel,
    SectionModel,
    VehicleStatusModel,
)


def _get_category(
    data: Optional[RemoteStatusModel], category: str
) -> Optional[VehicleStatusModel]:
    if data is not None:
        return next(
            (item for item in data.vehicle_status if item.category == category),
            None,
        )
    return None


def _get_section(data: Optional[VehicleStatusModel], section: str) -> Optional[SectionModel]:
    if data is not None:
        return next(
            (item for item in data.sections if item.section == section),
            None,
        )
    return None


def _get_status(data: Optional[SectionModel], status: str) -> Optional[bool]:
    if data is not None:
        item_status = next(
            (item.status for item in data.values if item.value == status),
            None,
        )
        return item_status if item_status is None else not bool(item_status)
    return None


class Door:
    """Door/hood data model."""

    def __init__(
        self,
        status: Optional[SectionModel] = None,
    ):
        """Initialise Door Model."""
        self._status = status or None

    def __repr__(self):
        """Representation of the model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def closed(self) -> Optional[bool]:
        """If the door is closed."""
        return _get_status(self._status, status="carstatus_closed")

    @property
    def locked(self) -> Optional[bool]:
        """If the door is locked."""
        if _get_status(self._status, status="carstatus_locked") is True:
            return True
        if _get_status(self._status, status="carstatus_unlocked") is False:
            return False
        else:
            return None


class Doors:
    """Trunk/doors/hood data model."""

    def __init__(
        self,
        status: Optional[RemoteStatusModel] = None,
    ):
        """Initialise Doors Model."""
        self._status = status or None

    def __repr__(self):
        """Representation of the model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def driver_seat(self) -> Optional[Door]:
        """Driver seat door."""
        category = _get_category(self._status, category="carstatus_category_driver")
        section = _get_section(category, section="carstatus_item_driver_door")
        return Door(section)

    @property
    def driver_rear_seat(self) -> Optional[Door]:
        """Right rearseat door."""
        category = _get_category(self._status, category="carstatus_category_driver")
        section = _get_section(category, section="carstatus_item_driver_rear_door")
        return Door(section)

    @property
    def passenger_seat(self) -> Optional[Door]:
        """Passenger seat door."""
        category = _get_category(self._status, category="carstatus_category_passenger")
        section = _get_section(category, section="carstatus_item_passenger_door")
        return Door(section)

    @property
    def passenger_rear_seat(self) -> Optional[Door]:
        """Left rearseat door."""
        category = _get_category(self._status, category="carstatus_category_passenger")
        section = _get_section(category, section="carstatus_item_passenger_rear_door")
        return Door(section)

    @property
    def trunk(self) -> Optional[Door]:
        """Trunk."""
        category = _get_category(self._status, category="carstatus_category_other")
        section = _get_section(category, section="carstatus_item_rear_hatch")
        return Door(section)


class Window(List[VehicleStatusModel]):
    """Window data model."""

    def __init__(
        self,
        status: Optional[SectionModel] = None,
    ):
        """Initialise Window Model."""
        self._status = status or None

    def __repr__(self):
        """Representation of the model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def closed(self) -> Optional[bool]:
        """Window closed state."""
        return _get_status(self._status, status="carstatus_closed")


class Windows:
    """Windows data model."""

    def __init__(
        self,
        status: Optional[RemoteStatusModel] = None,
    ):
        """Initialise Windows Model."""
        self._status = status or None

    def __repr__(self):
        """Representation of the model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def driver_seat(self) -> Optional[Window]:
        """Driver seat window."""
        category = _get_category(self._status, category="carstatus_category_driver")
        section = _get_section(category, section="carstatus_item_driver_window")
        return Window(section)

    @property
    def driver_rear_seat(self) -> Optional[Window]:
        """Right rearseat window."""
        category = _get_category(self._status, category="carstatus_category_driver")
        section = _get_section(category, section="carstatus_item_driver_rear_window")
        return Window(section)

    @property
    def passenger_seat(self) -> Optional[Window]:
        """Passenger seat window."""
        category = _get_category(self._status, category="carstatus_category_passenger")
        section = _get_section(category, section="carstatus_item_passenger_window")
        return Window(section)

    @property
    def passenger_rear_seat(self) -> Optional[Window]:
        """Left rearseat window."""
        category = _get_category(self._status, category="carstatus_category_passenger")
        section = _get_section(category, section="carstatus_item_passenger_rear_window")
        return Window(section)


class LockStatus:
    """Vehicle lock status data model."""

    def __init__(
        self,
        status: Optional[RemoteStatusResponseModel] = None,
    ):
        """Initialise LockStatus."""
        self._status = status.payload if status else None

    def __repr__(self):
        """Representation of the model."""
        return " ".join(
            [
                f"{k}={getattr(self, k)!s}"
                for k, v in type(self).__dict__.items()
                if isinstance(v, property)
            ],
        )

    @property
    def last_updated(self) -> Optional[datetime]:
        """Last time data was recieved from the car."""
        return self._status if self._status is None else self._status.occurrence_date

    @property
    def doors(self) -> Optional[Doors]:
        """Doors."""
        return self._status if self._status is None else Doors(self._status)

    @property
    def windows(self) -> Optional[Windows]:
        """Windows."""
        return self._status if self._status is None else Windows(self._status)

    @property
    def hood(self) -> Optional[Door]:
        """Hood."""
        if self._status is None:
            return None
        category = _get_category(self._status, category="carstatus_category_other")
        section = _get_section(category, section="carstatus_item_hood")
        return Door(section)

    # Seems to be not available for now
    # TODO: Calculate it from all other sensor values?
    # @property
    # def overallstatus(self) -> Optional[str]:
    #     """If a warning exists for any of the sensors."""
    #     return self._data.get("overallStatus")

    # Seems to be not available for now
    # @property
    # def lights(self) -> Optional[Lights]:
    #    """Lights."""
    #    return self._status if self._status is None else Lights(self._status.vehicle_status)

    # Seems to be not available for now
    # @property
    # def key(self) -> Key:
    #    """Key."""
    #    return Key(self._data.get("key"))
