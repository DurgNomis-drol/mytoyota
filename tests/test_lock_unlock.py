"""pytest tests for mytoyota.client.MyT sending lock/unlock requests"""
import asyncio
from datetime import datetime

import pytest

from mytoyota.exceptions import ToyotaActionNotSupported
from mytoyota.models.lock_unlock import (
    VehicleLockUnlockActionResponse,
    VehicleLockUnlockStatusResponse,
)
from tests.test_myt import TestMyTHelper


class TestLockUnlock(TestMyTHelper):
    """Pytest functions to test locking and unlocking"""

    successful_lock_request_id = "d4f873d2-5da2-494f-a6d9-6e56d18d2ce9"
    failed_lock_request_id = "14f873d2-5da2-494f-a6d9-6e56d18d2ce9"
    pending_lock_request_id = "24f873d2-5da2-494f-a6d9-6e56d18d2ce9"

    def test_send_lock_request(self):
        """Test sending the lock request"""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        result = asyncio.get_event_loop().run_until_complete(
            myt.set_lock_vehicle(vehicle["vin"])
        )
        assert isinstance(result, VehicleLockUnlockActionResponse)
        assert result.raw_json == {
            "id": self.pending_lock_request_id,
            "status": "inprogress",
            "type": "controlLock",
        }
        assert result.request_id == self.pending_lock_request_id
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
            "id": self.pending_lock_request_id,
            "status": "inprogress",
            "type": "controlLock",
        }

    def test_get_successful_lock_status(self):
        """Test getting the lock status"""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        result = asyncio.get_event_loop().run_until_complete(
            myt.get_lock_status(vehicle["vin"], self.successful_lock_request_id)
        )
        assert isinstance(result, VehicleLockUnlockStatusResponse)
        assert result.raw_json == {
            "id": self.successful_lock_request_id,
            "status": "completed",
            "requestTimestamp": "2022-10-22T08:49:20.071Z",
            "type": "controlLock",
        }
        assert result.request_id == self.successful_lock_request_id
        assert result.status == "completed"
        assert result.type == "controlLock"
        assert result.request_timestamp == datetime(2022, 10, 22, 8, 49, 20, 71000)
        assert not result.is_in_progress
        assert not result.is_error
        assert result.is_success

    def test_get_failed_lock_status(self):
        """Test getting the lock status"""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        result = asyncio.get_event_loop().run_until_complete(
            myt.get_lock_status(vehicle["vin"], self.failed_lock_request_id)
        )
        assert isinstance(result, VehicleLockUnlockStatusResponse)
        assert result.raw_json == {
            "id": self.failed_lock_request_id,
            "status": "error",
            "errorCode": "LU0004",
            "requestTimestamp": "2022-10-22T08:49:20.071Z",
            "type": "controlLock",
        }
        assert result.request_id == self.failed_lock_request_id
        assert result.status == "error"
        assert result.error_code == "LU0004"
        assert result.type == "controlLock"
        assert result.request_timestamp == datetime(2022, 10, 22, 8, 49, 20, 71000)
        assert not result.is_in_progress
        assert result.is_error
        assert not result.is_success

    def test_set_lock_vehicle_unsupported(self):
        """Test sending the lock request to a vehicle for which it is not supported"""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 1111111)
        with pytest.raises(ToyotaActionNotSupported):
            asyncio.get_event_loop().run_until_complete(
                myt.set_lock_vehicle(vehicle["vin"])
            )

    def test_set_unlock_vehicle_unsupported(self):
        """Test sending the lock request to a vehicle for which it is not supported"""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 1111111)
        with pytest.raises(ToyotaActionNotSupported):
            asyncio.get_event_loop().run_until_complete(
                myt.set_unlock_vehicle(vehicle["vin"])
            )
