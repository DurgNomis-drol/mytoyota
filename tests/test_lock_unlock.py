"""pytest tests for mytoyota.client.MyT sending lock/unlock requests"""
import asyncio
from datetime import datetime
import pytest

from mytoyota.models.lock_unlock import (
    VehicleLockUnlockActionResponse,
    VehicleLockUnlockStatusResponse,
)
from mytoyota.exceptions import ToyotaActionNotSupported
from tests.test_myt import TestMyTHelper


class TestLockUnlock(TestMyTHelper):
    """Pytest functions to test locking and unlocking"""

    _lock_request_id = "d4f873d2-5da2-494f-a6d9-6e56d18d2ce9"

    def test_send_lock_request(self):
        """Test sending the lock request"""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        result = asyncio.get_event_loop().run_until_complete(
            myt.set_lock_vehicle(vehicle["vin"])
        )
        assert isinstance(result, VehicleLockUnlockActionResponse)
        assert result.raw_json == {
            "id": self._lock_request_id,
            "status": "inprogress",
            "type": "controlLock",
        }
        assert result.request_id == self._lock_request_id
        assert result.status == "inprogress"
        assert result.type == "controlLock"

    def test_send_unlock_request(self):
        """Test sending the unlock request"""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        result = asyncio.get_event_loop().run_until_complete(
            myt.set_unlock_vehicle(vehicle["vin"])
        )
        assert isinstance(result, VehicleLockUnlockActionResponse)
        assert result.raw_json == {
            "id": self._lock_request_id,
            "status": "inprogress",
            "type": "controlLock",
        }

    def test_get_lock_status(self):
        """Test getting the lock status"""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        result = asyncio.get_event_loop().run_until_complete(
            myt.get_lock_status(vehicle["vin"], self._lock_request_id)
        )
        assert isinstance(result, VehicleLockUnlockStatusResponse)
        assert result.raw_json == {
            "id": self._lock_request_id,
            "status": "completed",
            "requestTimestamp": "2022-10-22T08:49:20.071Z",
            "type": "controlLock",
        }
        assert result.request_id == self._lock_request_id
        assert result.status == "completed"
        assert result.type == "controlLock"
        assert result.request_timestamp == datetime(2022, 10, 22, 8, 49, 20, 71000)

    def test_set_lock_vehicle_unsupported(self):
        """Test sending the lock request to a vehicle for which it is not supported"""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 1111111)
        with pytest.raises(ToyotaActionNotSupported):
            result = asyncio.get_event_loop().run_until_complete(
                myt.set_lock_vehicle(vehicle["vin"])
            )

    def test_set_unlock_vehicle_unsupported(self):
        """Test sending the lock request to a vehicle for which it is not supported"""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 1111111)
        with pytest.raises(ToyotaActionNotSupported):
            result = asyncio.get_event_loop().run_until_complete(
                myt.set_unlock_vehicle(vehicle["vin"])
            )

