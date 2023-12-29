"""Test lock_status Model."""
from datetime import datetime

import pytest

from mytoyota.models.endpoints.common import UnitValueModel
from mytoyota.models.endpoints.status import (
    RemoteStatusModel,
    RemoteStatusResponseModel,
    SectionModel,
    VehicleStatusModel,
    _TelemetryModel,
    _ValueStatusModel,
)
from mytoyota.models.lock_status import Door, Doors, LockStatus, Window, Windows

# Mock data for testing
mock_section_closed = SectionModel(
    section="carstatus_item_driver_door",
    values=[_ValueStatusModel(value="carstatus_closed", status=0)],
)
mock_section_locked = SectionModel(
    section="carstatus_item_driver_door",
    values=[_ValueStatusModel(value="carstatus_locked", status=0)],
)
mock_vehicle_status = VehicleStatusModel(
    category="carstatus_category_driver",
    sections=[mock_section_closed, mock_section_locked],
    displayOrder=1,
)
mock_remote_status = RemoteStatusModel(
    vehicleStatus=[mock_vehicle_status],
    latitude=1.0,
    longitude=1.0,
    occurrenceDate=datetime.now().replace(second=0, microsecond=0),
    locationAcquisitionDatetime=datetime.now().replace(second=0, microsecond=0),
    cautionOverallCount=1,
    telemetry=_TelemetryModel(
        fugage=UnitValueModel(unit="bla", value=1.0),
        rage=UnitValueModel(unit="bla", value=1.0),
        odo=UnitValueModel(unit="bla", value=1.0),
    ),
)
mock_remote_status_response = RemoteStatusResponseModel(
    payload=mock_remote_status, status="OK", code=200, errors=[], message=None
)


# Parametrized test for Door.closed property
@pytest.mark.parametrize(
    "section, expected",
    [
        (None, None),  # No section provided
        (mock_section_closed, True),  # Door is closed
        (mock_section_locked, None),  # Status not related to closed
    ],
    ids=["no-section", "door-closed", "unrelated-status"],
)
def test_door_closed(section, expected):  # noqa: D103
    # Arrange
    door = Door(status=section)

    # Act
    result = door.closed

    # Assert
    assert result == expected


# Parametrized test for Door.locked property
@pytest.mark.parametrize(
    "section, expected",
    [
        (None, None),  # No section provided
        (mock_section_locked, True),  # Door is locked
        (mock_section_closed, None),  # Status not related to locked
    ],
    ids=["no-section", "door-locked", "unrelated-status"],
)
def test_door_locked(section, expected):  # noqa: D103
    # Arrange
    door = Door(status=section)

    # Act
    result = door.locked

    # Assert
    assert result == expected


# Parametrized test for Doors properties
@pytest.mark.parametrize(
    "category, section_name, property_name, expected_class",
    [
        (
            "carstatus_category_driver",
            "carstatus_item_driver_door",
            "driver_seat",
            Door,
        ),
        (
            "carstatus_category_passenger",
            "carstatus_item_passenger_door",
            "passenger_seat",
            Door,
        ),
        ("carstatus_category_other", "carstatus_item_rear_hatch", "trunk", Door),
    ],
    ids=["driver-seat", "passenger-seat", "trunk"],
)
def test_doors_properties(  # noqa : D103
    category, section_name, property_name, expected_class
):
    # Arrange
    status = RemoteStatusModel(
        vehicleStatus=[
            VehicleStatusModel(
                category=category,
                sections=[
                    SectionModel(
                        section=section_name,
                        values=[_ValueStatusModel(value="carstatus_locked", status=0)],
                    )
                ],
                displayOrder=1,
            )
        ],
        latitude=1.0,
        longitude=1.0,
        occurrenceDate=datetime.now().replace(second=0, microsecond=0),
        locationAcquisitionDatetime=datetime.now(),
        cautionOverallCount=1,
        telemetry=_TelemetryModel(
            fugage=UnitValueModel(unit="bla", value=1.0),
            rage=UnitValueModel(unit="bla", value=1.0),
            odo=UnitValueModel(unit="bla", value=1.0),
        ),
    )

    # Act
    doors = Doors(status=status)
    result = getattr(doors, property_name)

    # Assert
    assert isinstance(result, expected_class)


# Parametrized test for Window.closed property
@pytest.mark.parametrize(
    "section, expected",
    [
        (None, None),  # No section provided
        (mock_section_closed, True),  # Window is closed
    ],
    ids=["no-section", "window-closed"],
)
def test_window_closed(section, expected):  # noqa: D103
    # Arrange
    window = Window(status=section)

    # Act
    result = window.closed

    # Assert
    assert result == expected


# Parametrized test for Windows properties
@pytest.mark.parametrize(
    "category, section_name, property_name, expected_class",
    [
        (
            "carstatus_category_driver",
            "carstatus_item_driver_window",
            "driver_seat",
            Window,
        ),
        (
            "carstatus_category_passenger",
            "carstatus_item_passenger_window",
            "passenger_seat",
            Window,
        ),
    ],
    ids=["driver-seat-window", "passenger-seat-window"],
)
def test_windows_properties(  # noqa : D103
    category, section_name, property_name, expected_class
):
    # Arrange
    status = RemoteStatusModel(
        vehicleStatus=[
            VehicleStatusModel(
                category=category,
                sections=[
                    SectionModel(
                        section=section_name,
                        values=[_ValueStatusModel(value="carstatus_locked", status=0)],
                    )
                ],
                displayOrder=1,
            )
        ],
        latitude=1.0,
        longitude=1.0,
        occurrenceDate=datetime.now().replace(second=0, microsecond=0),
        locationAcquisitionDatetime=datetime.now(),
        cautionOverallCount=1,
        telemetry=_TelemetryModel(
            fugage=UnitValueModel(unit="bla", value=1.0),
            rage=UnitValueModel(unit="bla", value=1.0),
            odo=UnitValueModel(unit="bla", value=1.0),
        ),
    )

    # Act
    windows = Windows(status=status)
    result = getattr(windows, property_name)

    # Assert
    assert isinstance(result, expected_class)


# Parametrized test for LockStatus properties
@pytest.mark.parametrize(
    "status, expected_last_updated, expected_doors_class, expected_windows_class",
    [
        (None, None, None, None),  # No status provided
        (
            mock_remote_status_response,
            datetime.now().replace(second=0, microsecond=0),
            Doors,
            Windows,
        ),  # Valid status
    ],
    ids=["no-status", "valid-status"],
)
def test_lock_status_properties(  # noqa : D103
    status, expected_last_updated, expected_doors_class, expected_windows_class
):
    # Arrange
    lock_status = LockStatus(status=status)

    # Act & Assert
    assert lock_status.last_updated == expected_last_updated
    assert (
        isinstance(lock_status.doors, expected_doors_class)
        if expected_doors_class
        else lock_status.doors is None
    )
    assert (
        isinstance(lock_status.windows, expected_windows_class)
        if expected_windows_class
        else lock_status.windows is None
    )
