"""Simple test of new API Changes."""
import asyncio
import json
import pprint
from datetime import date, timedelta

from mytoyota.client import MyT
from mytoyota.models.endpoints.climate import ACOperations, ACParameters, ClimateSettingsModel
from mytoyota.models.endpoints.command import CommandType
from mytoyota.models.summary import SummaryType

pp = pprint.PrettyPrinter(indent=4)


# Set your username and password in a file on top level called "credentials.json" in the format:
#   {
#       "username": "<username>",
#       "password": "<password>"
#   }


def load_credentials():
    """Load credentials from 'credentials.json'."""
    try:
        with open("credentials.json", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return None


credentials = load_credentials()
if not credentials:
    raise ValueError(
        "Did you forget to set your username and password? Or supply the credentials file"
    )

USERNAME = credentials["username"]
PASSWORD = credentials["password"]

client = MyT(username=USERNAME, password=PASSWORD)


async def get_information():
    """Test login and output from endpoints."""
    print("Logging in...")
    await client.login()

    print("Retrieving cars...")
    cars = await client.get_vehicles(metric=True)

    for car in cars:

        # Send command to car
        # pp.pprint(await car.post_command(command=CommandType.DOOR_LOCK))
        # return

        # Get climate status
        # response = await car._api.get_climate_status_endpoint(car.vin)
        # print(response)

        # Get current climate settings
        # settings = await car._api.get_climate_settings_endpoint(car.vin)
        # print(settings)
        # climate_settings: ClimateSettingsModel = ClimateSettingsModel(
        #   settingsOn=True,
        #   temperature=21,
        #   temperatureUnit="C",
        #   acOperations=[ACOperations(
        #       categoryName="defrost",
        #       acParameters=[ACParameters(enabled=True, name="frontDefrost"),
        #       ACParameters(enabled=False, name="rearDefrost")])])
        # climate_settings = settings.payload
        # climate_settings.temperature = 20
        # response = await car._api.put_climate_settings_endpoint(car.vin, climate_settings)
        # print(response)
        # return

        await car.update()

        # Dashboard Information
        pp.pprint(f"Dashboard: {car.dashboard}")
        # Electric Status Information
        pp.pprint(f"Electric Status: {car.electric_status}")
        # Location Information
        pp.pprint(f"Location: {car.location}")
        # Lock Status
        pp.pprint(f"Lock Status: {car.lock_status}")
        # Notifications
        pp.pprint(f"Notifications: {[[x] for x in car.notifications]}")
        # Service history
        pp.pprint(f"Latest service: {car.get_latest_service_history()}")
        # Summary
        # pp.pprint(
        #    f"Summary: {[[x] for x in await car.get_summary(date.today() - timedelta(days=7), date.today(), summary_type=SummaryType.DAILY)]}"  # noqa: E501 # pylint: disable=C0301
        # )
        # pp.pprint(
        #    f"Summary: {[[x] for x in await car.get_summary(date.today() - timedelta(days=7 * 4), date.today(), summary_type=SummaryType.WEEKLY)]}"  # noqa: E501 # pylint: disable=C0301
        # )
        pp.pprint(
            f"Summary: {[[x] for x in await car.get_summary(date.today() - timedelta(days=6 * 30), date.today(), summary_type=SummaryType.MONTHLY)]}"  # noqa: E501
        )
        # pp.pprint(
        #    f"Summary: {[[x] for x in await car.get_summary(date.today() - timedelta(days=365), date.today(), summary_type=SummaryType.YEARLY)]}"  # noqa: E501 # pylint: disable=C0301
        # )

        # Trips
        # pp.pprint(
        #    f"Trips: f{await car.get_trips(date.today() - timedelta(days=7), date.today(), full_route=True)}"  # noqa: E501
        # )

        # Dump all the information collected so far:
        # pp.pprint(car._dump_all())


loop = asyncio.get_event_loop()
loop.run_until_complete(get_information())
loop.close()
