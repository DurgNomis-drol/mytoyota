"""pytest tests for mytoyota.client.MyT."""

import asyncio
import datetime
import json
import os
import os.path
import re
from typing import Optional, Union

import arrow
import pytest  # pylint: disable=import-error

from mytoyota.client import MyT
from mytoyota.exceptions import (
    ToyotaActionNotSupportedError,
    ToyotaInternalError,
    ToyotaInvalidUsernameError,
    ToyotaLocaleNotValid,
    ToyotaRegionNotSupportedError,
)
from mytoyota.models.trip import DetailedTrip, Trip, TripEvent


class OfflineController:
    """Provides a Controller class that can be used for testing."""

    def __init__(  # noqa: PLR0913
        self,
        locale: str,
        region: str,
        username: str,
        password: str,
        brand: str,
        uuid: str = None,
    ) -> None:
        """Initialise offline controller class."""
        self._locale = locale
        self._region = region
        self._username = username
        self._password = password
        self._brand = brand
        self._uuid = uuid

    @property
    def uuid(self) -> str:
        """Returns uuid."""
        return "_OfflineController_"

    async def first_login(self) -> None:
        """Perform first login."""
        # This is no-operation

    def _load_from_file(self, filename: str):
        """Load and return data structure from specified JSON filename."""
        with open(filename, encoding="UTF-8") as json_file:
            return json.load(json_file)

    # Disables pylint warning about too many statements and branches when matching API paths
    async def request(  # noqa: PLR0912, PLR0913, PLR0915
        self,
        method: str,
        endpoint: str,
        base_url: Optional[str] = None,
        body: Optional[dict] = None,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> Union[dict, list, None]:
        """Shared request method."""
        if method not in ("GET", "POST", "PUT", "DELETE"):
            raise ToyotaInternalError("Invalid request method provided")  # pragma: no cover

        _ = base_url

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

        match = re.match(r"/vehicle/user/.*/vehicle/([^?]+)\?.*services=fud,connected", endpoint)
        if match:
            vin = match.group(1)
            response = self._load_from_file(os.path.join(data_files, f"vehicle_{vin}_connected_services.json"))

        match = re.match(r".*/vehicle/([^/]+)/addtionalInfo", endpoint)
        if match:
            vin = match.group(1)
            response = self._load_from_file(os.path.join(data_files, f"vehicle_{vin}_odometer.json"))

        match = re.match(r".*/vehicles/([^/]+)/vehicleStatus", endpoint)
        if match:
            vin = match.group(1)
            response = self._load_from_file(os.path.join(data_files, f"vehicle_{vin}_status.json"))

        match = re.match(r".*/vehicles/([^/]+)/remoteControl/status", endpoint)
        if match:
            vin = match.group(1)
            response = self._load_from_file(os.path.join(data_files, f"vehicle_{vin}_status_legacy.json"))

        match = re.match(r"/v2/trips/summarize", endpoint)
        if match:
            # We should retrieve the driving statistics
            vin = headers["vin"]
            interval = params["calendarInterval"]
            response = self._load_from_file(os.path.join(data_files, f"vehicle_{vin}_statistics_{interval}.json"))

        match = re.match(r"/api/user/.*/cms/trips/v2/history/vin/([^?]+)/.*", endpoint)
        if match:
            # We should retrieve the trips
            vin = match.group(1)
            response = self._load_from_file(os.path.join(data_files, f"vehicle_{vin}_trips.json"))

        match = re.match(r"/api/user/.*/cms/trips/v2/([^?]+)/events/vin/([^?]+)", endpoint)
        if match:
            # We should retrieve the trips
            trip_id = match.group(1)
            vin = match.group(2)
            response = self._load_from_file(os.path.join(data_files, f"vehicle_{vin}_trip_{trip_id}.json"))

        match = re.match(r".*/vehicles/([^?]+)/lock", endpoint)
        if match:
            vin = match.group(1)
            try:
                response = self._load_from_file(os.path.join(data_files, f"vehicle_{vin}_lock_request.json"))
            except FileNotFoundError as exc:
                raise ToyotaActionNotSupportedError("Action is not supported") from exc

        match = re.match(r".*/vehicles/([^?]+)/lock/([^?]+)", endpoint)
        if match:
            vin = match.group(1)
            request_id = match.group(2)
            response = self._load_from_file(
                os.path.join(data_files, f"vehicle_{vin}_lock_request_status_{request_id}.json")
            )
        return response


class TestMyTHelper:
    """Helper class for the actual TestMyT pytest classes."""

    def _create_offline_myt(self) -> MyT:
        """Create a MyT instance that is using the OfflineController."""
        return MyT(
            username="user@domain.com",
            password="xxxxx",
            locale="en-gb",
            region="europe",
            controller_class=OfflineController,
        )

    def _lookup_vehicle(self, myt: MyT, vehicle_id: int):
        """Retrieve all the vehicles, and find the vehicle with the specified 'id'."""
        vehicles = asyncio.get_event_loop().run_until_complete(myt.get_vehicles())
        vehicle = [veh for veh in vehicles if veh["id"] == vehicle_id]
        return vehicle[0]


class TestMyT(TestMyTHelper):
    """pytest functions to test MyT."""

    def test_myt(self):
        """Test an error free initialisation of MyT."""
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
        """Test an invalid username in MyT."""
        with pytest.raises(ToyotaInvalidUsernameError):
            _ = MyT(username=username, password="xxxxx", locale="en-gb", region="europe")

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
        """Test an invalid locale in MyT."""
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
        """Test an invalid region in MyT."""
        with pytest.raises(ToyotaRegionNotSupportedError):
            _ = MyT(
                username="user@domain.com",
                password="xxxxx",
                locale="en-gb",
                region=region,
            )

    def test_get_supported_regions(self):
        """Test the supported regions."""
        regions = MyT.get_supported_regions()
        assert regions is not None
        assert len(regions) > 0
        assert "europe" in regions

    def test_login(self):
        """Test the login."""
        myt = self._create_offline_myt()
        asyncio.get_event_loop().run_until_complete(myt.login())

    def test_get_uuid(self):
        """Test the retrieval of an uuid."""
        myt = self._create_offline_myt()
        uuid = myt.uuid
        assert uuid
        assert len(uuid) > 0

    def test_set_alias(self):
        """Test the set_alias."""
        myt = self._create_offline_myt()
        result = asyncio.get_event_loop().run_until_complete(myt.set_alias(4444444, "pytest_vehicle"))
        assert isinstance(result, (dict))
        assert result == {"id": "4444444", "alias": "pytest_vehicle"}

    def test_get_vehicles(self):
        """Test the retrieval of the available vehicles."""
        myt = self._create_offline_myt()
        vehicles = asyncio.get_event_loop().run_until_complete(myt.get_vehicles())
        assert vehicles
        assert len(vehicles) > 0
        for veh in vehicles:
            assert isinstance(veh, (dict))
            assert len(veh.keys()) > 0

    def test_get_vehicles_json(self):
        """Test the retrieval of the available vehicles in json format."""
        myt = self._create_offline_myt()
        vehicles_json = asyncio.get_event_loop().run_until_complete(myt.get_vehicles_json())
        assert json.loads(vehicles_json) is not None

    def test_get_vehicle_status(self):
        """Test the retrieval of the status of a vehicle."""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        # Retrieve the actual status of the vehicle
        status = asyncio.get_event_loop().run_until_complete(myt.get_vehicle_status(vehicle))
        assert status is not None

    def test_get_trips_json(self):
        """Test the retrieval of the trips of a vehicle."""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        # Retrieve the actual trips of the vehicle
        trips = asyncio.get_event_loop().run_until_complete(myt.get_trips_json(vehicle["vin"]))
        assert trips is not None

    def test_get_trip_json(self):
        """Test the retrieval of a trip of a vehicle."""
        trip_id = "971B8221-299E-4899-BC73-AE2EFF604D28"
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        trip_json = asyncio.get_event_loop().run_until_complete(myt.get_trip_json(vehicle["vin"], trip_id))
        assert trip_json is not None

    def test_get_trips(self):
        """Test the retrieval of the trips of a vehicle."""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        trips = asyncio.get_event_loop().run_until_complete(myt.get_trips(vehicle["vin"]))
        assert trips is not None
        for trip in trips:
            assert isinstance(trip, Trip)
            assert trip.raw_json.get("tripId") is not None
            assert isinstance(trip.trip_id, str)
            assert trip.raw_json.get("startAddress") is not None
            assert isinstance(trip.start_address, str)
            assert trip.raw_json.get("endAddress") is not None
            assert isinstance(trip.end_address, str)
            assert trip.raw_json.get("startTimeGmt") is not None
            assert isinstance(trip.start_time_gmt, datetime.datetime)
            assert trip.raw_json.get("endTimeGmt") is not None
            assert isinstance(trip.end_time_gmt, datetime.datetime)
            assert trip.raw_json.get("classificationType") is not None
            assert isinstance(trip.classification_type, int)

    def test_get_trip(self):
        """Test the retrieval of a trip of a vehicle."""
        trip_id = "971B8221-299E-4899-BC73-AE2EFF604D28"
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        # Retrieve the actual trip
        trip = asyncio.get_event_loop().run_until_complete(myt.get_trip(vehicle["vin"], trip_id))
        assert trip is not None
        assert isinstance(trip, DetailedTrip)
        assert len(trip.trip_events) == 12
        for event in trip.trip_events:
            assert isinstance(event, TripEvent)
            assert event.raw_json.get("lat") is not None
            assert isinstance(event.latitude, float)
            assert event.raw_json.get("lon") is not None
            assert isinstance(event.longitude, float)
            assert event.raw_json.get("overspeed") is not None
            assert isinstance(event.overspeed, bool)
            assert event.raw_json.get("isEv") is not None
            assert isinstance(event.is_ev, bool)
            assert event.raw_json.get("highway") is not None
            assert isinstance(event.highway, bool)
            assert event.raw_json.get("mode") is not None
            assert isinstance(event.mode, int)
        assert trip.raw_json.get("statistics") is not None
        assert isinstance(trip.statistics, dict)


class TestMyTStatistics(TestMyTHelper):
    """pytest functions to test get_vehicle_statistics of MyT."""

    def test_get_vehicle_statistics_invalid_interval_error(self):
        """Test that retrieving the statistics of an unknown interval is not possible."""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        # Retrieve the actual status of the vehicle
        stat = asyncio.get_event_loop().run_until_complete(myt.get_driving_statistics(vehicle["vin"], "century"))
        assert stat is not None
        assert "error_mesg" in stat[0]

    def test_get_vehicle_statistics_tomorrow_error(self):
        """Test that retrieving the statistics of tomorrow is not possible."""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        tomorrow = arrow.now().shift(days=1).format("YYYY-MM-DD")
        # Retrieve the actual status of the vehicle
        stat = asyncio.get_event_loop().run_until_complete(
            myt.get_driving_statistics(vehicle["vin"], "year", from_date=tomorrow)
        )
        assert stat is not None
        assert "error_mesg" in stat[0]

    def test_get_vehicle_statistics_isoweek_error(self):
        """Test that retrieving statistics of long ago of an isoweek is not possible."""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        # Retrieve the actual status of the vehicle
        stat = asyncio.get_event_loop().run_until_complete(
            myt.get_driving_statistics(vehicle["vin"], "isoweek", from_date="2010-01-01")
        )
        assert stat is not None
        assert "error_mesg" in stat[0]

    def test_get_vehicle_statistics_year_error(self):
        """Test that retrieving the previous year is not possible."""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        previous_year = arrow.now().shift(years=-1).format("YYYY-MM-DD")
        # Retrieve the actual status of the vehicle
        stat = asyncio.get_event_loop().run_until_complete(
            myt.get_driving_statistics(vehicle["vin"], "year", from_date=previous_year)
        )
        assert stat is not None
        assert "error_mesg" in stat[0]

    @pytest.mark.parametrize(
        "interval,unit",
        [
            ("day", "metric"),
            ("day", "imperial"),
            ("day", "imperial_liters"),
            ("week", "metric"),
            ("week", "imperial"),
            ("week", "imperial_liters"),
            ("isoweek", "metric"),
            ("isoweek", "imperial"),
            ("isoweek", "imperial_liters"),
            ("month", "metric"),
            ("month", "imperial"),
            ("month", "imperial_liters"),
            # Retrieving the year statistics of today is possible
            # as it will get the current year statistics
        ],
    )
    def test_get_vehicle_statistics_today_error(self, interval, unit):
        """Test that retrieving the statistics of today is not possible."""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        today = arrow.now().format("YYYY-MM-DD")
        # Retrieve the actual status of the vehicle
        stat = asyncio.get_event_loop().run_until_complete(
            myt.get_driving_statistics(vehicle["vin"], interval, unit=unit, from_date=today)
        )
        assert stat is not None
        assert "error_mesg" in stat[0]

    @pytest.mark.parametrize(
        "interval,unit",
        [
            ("day", "metric"),
            ("day", "imperial"),
            ("day", "imperial_liters"),
            #            ("week", "metric"),
            #            ("week", "imperial"),
            #            ("week", "imperial_liters"),
            #            ("isoweek", "metric"),
            #            ("isoweek", "imperial"),
            #            ("isoweek", "imperial_liters"),
            ("month", "metric"),
            ("month", "imperial"),
            ("month", "imperial_liters"),
            ("year", "metric"),
            ("year", "imperial"),
            ("year", "imperial_liters"),
        ],
    )
    def test_get_driving_statistics(self, interval, unit):
        """Test the retrieval of the status of a vehicle."""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        # Retrieve the actual status of the vehicle
        statistics = asyncio.get_event_loop().run_until_complete(
            myt.get_driving_statistics(vehicle["vin"], interval, unit=unit)
        )
        assert statistics is not None
        for data in statistics:
            assert data["bucket"] is not None
            # And the unit should be requested unit
            assert data["bucket"]["unit"] == unit
            # And the year should be recent or (short) future
            assert 2018 <= int(data["bucket"]["year"]) <= 2100
            assert data["data"] is not None

    @pytest.mark.parametrize(
        "unit",
        [
            ("metric"),
            ("imperial"),
            ("imperial_liters"),
        ],
    )
    def test_get_driving_statistics_has_correct_day_of_year(self, unit):
        """Test that the day-statistics contains the correct date for the day of the year."""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        # Retrieve the driving statistics of the vehicle
        statistics = asyncio.get_event_loop().run_until_complete(
            myt.get_driving_statistics(vehicle["vin"], "day", unit=unit)
        )
        assert statistics is not None
        for day_data in statistics:
            bucket = day_data["bucket"]
            date = datetime.date.fromisoformat(bucket["date"])
            day_of_year = int(date.strftime("%j"))
            assert bucket["dayOfYear"] == day_of_year
            assert int(bucket["year"]) == date.year

    @pytest.mark.parametrize(
        "interval,unit",
        [
            ("day", "metric"),
            ("day", "imperial"),
            ("day", "imperial_liters"),
            #            ("week", "metric"),
            #            ("week", "imperial"),
            #            ("week", "imperial_liters"),
            #            ("isoweek", "metric"),
            #            ("isoweek", "imperial"),
            #            ("isoweek", "imperial_liters"),
            ("month", "metric"),
            ("month", "imperial"),
            ("month", "imperial_liters"),
            ("year", "metric"),
            ("year", "imperial"),
            ("year", "imperial_liters"),
        ],
    )
    def test_get_driving_statistics_contains_year_as_int(self, interval, unit):
        """Test that the statistics contains the year as an integer."""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        # Retrieve the driving statistics of the vehicle
        statistics = asyncio.get_event_loop().run_until_complete(
            myt.get_driving_statistics(vehicle["vin"], interval, unit=unit)
        )
        assert statistics is not None
        for day_data in statistics:
            bucket = day_data["bucket"]
            assert isinstance(bucket["year"], int)

    @pytest.mark.parametrize(
        "interval",
        [
            ("day"),
            #           ("week"),
            #           ("isoweek"),
            ("month"),
            ("year"),
        ],
    )
    def test_get_driving_statistics_json(self, interval):
        """Test the retrieval of the statistics (in JSON format) of a vehicle."""
        myt = self._create_offline_myt()
        vehicle = self._lookup_vehicle(myt, 4444444)
        assert vehicle is not None
        # Retrieve the actual status of the vehicle
        statistics_json = asyncio.get_event_loop().run_until_complete(
            myt.get_driving_statistics_json(vehicle["vin"], interval)
        )
        assert json.loads(statistics_json) is not None
