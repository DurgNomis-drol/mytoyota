"""pytest tests for mytoyota.client.MyT"""

import asyncio
import json
import os.path
import re
from typing import Optional, Union

import pytest  # pylint: disable=import-error

from mytoyota.client import MyT
from mytoyota.exceptions import (
    ToyotaInternalError,
    ToyotaInvalidUsername,
    ToyotaLocaleNotValid,
    ToyotaRegionNotSupported,
)

# pylint: disable=no-self-use


class OfflineController:
    """Provides a Controller class that can be used for testing."""

    def __init__(
        self,
        locale: str,
        region: str,
        username: str,
        password: str,
        uuid: str = None,
    ) -> None:
        self._locale = locale
        self._region = region
        self._username = username
        self._password = password
        self._uuid = uuid

    async def get_uuid(self) -> str:
        """Returns uuid"""
        return "_OfflineController_"

    async def first_login(self) -> None:
        """Perform first login"""
        # This is no-operation

    def _load_from_file(self, filename: str):
        """Load a data structure from the specified JSON filename, and
        return it."""
        with open(filename, encoding="UTF-8") as json_file:
            return json.load(json_file)

    async def request(
        self,
        method: str,
        endpoint: str,
        base_url: Optional[str] = None,
        body: Optional[dict] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> Union[dict, list, None]:
        """Shared request method"""

        if method not in ("GET", "POST", "PUT", "DELETE"):
            raise ToyotaInternalError("Invalid request method provided")

        _ = base_url
        _ = params
        _ = headers

        data_files = os.path.join(os.path.curdir, "tests", "data")

        response = None

        match = re.match(r"/api/users/.*/vehicles/.*", endpoint)
        if match:
            # A new alias is set
            # We should return a predefined dictionary
            response = {"id": str(body["id"]), "alias": body["alias"]}

        match = re.match(r".*/vehicles\?.*services=uio", endpoint)
        if match:
            response = self._load_from_file(os.path.join(data_files, "vehicles.json"))

        match = re.match(
            r"/vehicle/user/.*/vehicle/([^?]+)\?.*services=fud,connected", endpoint
        )
        if match:
            vin = match.group(1)
            response = self._load_from_file(
                os.path.join(data_files, f"vehicle_{vin}_connected_services.json")
            )

        match = re.match(r".*/vehicle/([^/]+)/addtionalInfo", endpoint)
        if match:
            vin = match.group(1)
            response = self._load_from_file(
                os.path.join(data_files, f"vehicle_{vin}_odometer.json")
            )

        match = re.match(r".*/vehicles/([^/]+)/vehicleStatus", endpoint)
        if match:
            vin = match.group(1)
            response = self._load_from_file(
                os.path.join(data_files, f"vehicle_{vin}_status.json")
            )

        match = re.match(r".*/vehicles/([^/]+)/remoteControl/status", endpoint)
        if match:
            vin = match.group(1)
            response = self._load_from_file(
                os.path.join(data_files, f"vehicle_{vin}_status_legacy.json")
            )

        return response


class TestMyT:
    """pytest functions to test MyT"""

    def test_myt(self):
        """Test an error free initialisation of MyT"""
        myt = MyT(
            username="user@domain.com",
            password="xxxxx",
            locale="en-gb",
            region="europe",
        )
        assert myt is not None
        assert myt.api is not None

    @pytest.mark.parametrize(
        "username",
        [None, "", "_invalid_"],
    )
    def test_myt_invalid_username(self, username):
        """Test an invalid username in MyT"""
        with pytest.raises(ToyotaInvalidUsername):
            _ = MyT(
                username=username, password="xxxxx", locale="en-gb", region="europe"
            )

    @pytest.mark.parametrize(
        "locale",
        [
            None,
            "",
            "invalid-locale",
            "da-en-dk-us",
        ],
    )
    def test_myt_invalid_locale(self, locale):
        """Test an invalid locale in MyT"""
        with pytest.raises(ToyotaLocaleNotValid):
            _ = MyT(
                username="user@domain.com",
                password="xxxxx",
                locale=locale,
                region="europe",
            )

    @pytest.mark.parametrize(
        "region",
        [
            None,
            "",
            "antartica",
            "mars",
        ],
    )
    def test_myt_unsupported_region(self, region):
        """Test an invalid region in MyT"""
        with pytest.raises(ToyotaRegionNotSupported):
            _ = MyT(
                username="user@domain.com",
                password="xxxxx",
                locale="en-gb",
                region=region,
            )

    def test_get_supported_regions(self):
        """Test the supported regions"""
        regions = MyT.get_supported_regions()
        assert regions is not None
        assert len(regions) > 0
        assert "europe" in regions

    def _create_offline_myt(self) -> MyT:
        """Create a MyT instance that is using the OfflineController"""
        return MyT(
            username="user@domain.com",
            password="xxxxx",
            locale="en-gb",
            region="europe",
            controller_class=OfflineController,
        )

    def test_login(self):
        """Test the login"""
        myt = self._create_offline_myt()
        asyncio.get_event_loop().run_until_complete(myt.login())

    def test_get_uuid(self):
        """Test the retrieval of an uuid"""
        myt = self._create_offline_myt()
        uuid = asyncio.get_event_loop().run_until_complete(myt.get_uuid())
        assert uuid
        assert len(uuid) > 0

    def test_set_alias(self):
        """Test the set_alias"""
        myt = self._create_offline_myt()
        result = asyncio.get_event_loop().run_until_complete(
            myt.set_alias(4444444, "pytest_vehicle")
        )
        assert isinstance(result, (dict))
        assert result == {"id": "4444444", "alias": "pytest_vehicle"}

    def test_get_vehicles(self):
        """Test the retrieval of the available vehicles"""
        myt = self._create_offline_myt()
        vehicles = asyncio.get_event_loop().run_until_complete(myt.get_vehicles())
        assert vehicles
        assert len(vehicles) > 0
        for veh in vehicles:
            assert isinstance(veh, (dict))
            assert len(veh.keys()) > 0

    def test_get_vehicles_json(self):
        """Test the retrieval of the available vehicles in json format"""
        myt = self._create_offline_myt()
        vehicles_json = asyncio.get_event_loop().run_until_complete(
            myt.get_vehicles_json()
        )
        assert json.loads(vehicles_json) is not None

    def _lookup_vehicle(self, myt: MyT, vehicle_id: int):
        """Retrieve all the vehicles, and find the vehicle with the specified 'id'"""
        vehicles = asyncio.get_event_loop().run_until_complete(myt.get_vehicles())
        vehicle = [veh for veh in vehicles if veh["id"] == vehicle_id]
        return vehicle[0]

    def test_get_vehicle_status(self):
        """Test the retrieval of the status of a vehicle"""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        # Retrieve the actual status of the vehicle
        status = asyncio.get_event_loop().run_until_complete(
            myt.get_vehicle_status(vehicle)
        )
        assert status is not None

    def disabled___test_get_vehicle_status_json(self):
        """Test the retrieval of the status of a vehicle"""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        # Retrieve the actual status of the vehicle
        status_json = asyncio.get_event_loop().run_until_complete(
            myt.get_vehicle_status_json(vehicle)
        )
        assert json.loads(status_json) is not None
