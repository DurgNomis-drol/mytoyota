"""Simple test of new API Changes."""
import asyncio
import json
import pprint

from mytoyota.client import MyT

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
    raise ValueError("Did you forget to set your username and password? Or supply the credentials file")

USERNAME = credentials["username"]
PASSWORD = credentials["password"]

client = MyT(username=USERNAME, password=PASSWORD)


async def get_information():
    """Test login and output from endpoints."""
    print("Logging in...")
    await client.login()

    print("Retrieving cars...")
    cars = await client.get_vehicles(metric=False)

    for car in cars:
        await car.update()

        # Dashboard Information
        print(f"Dashboard: {car.dashboard}")
        # Location Information
        print(f"Location: {car.location}")
        # Notifications
        print(f"Notifications: {[x for x in car.notifications]}")

        # Dump all the information collected so far


#        pp.pprint(car._dump_all())  # pylint: disable=W0212


loop = asyncio.get_event_loop()
loop.run_until_complete(get_information())
loop.close()
