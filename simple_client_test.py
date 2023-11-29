import asyncio
import json
import pprint

from mytoyota.client import MyT

# Set your username and password here OR
# in a file called credentials.json in the format
#   {
#       "username": "<username>",
#       "password": "<password>"
#   }
username = None
password = None
try:
    credentials = json.load(open("credentials.json"))
    username = credentials["username"]
    password = credentials["password"]
except FileNotFoundError:
    pass
except json.decoder.JSONDecodeError:
    pass

if username is None or password is None:
    print(
        "Did you forget to set your username and password? Or supply the credentials file"
    )
    exit()

# Pretty Printer used below
pp = pprint.PrettyPrinter(indent=4)


client = MyT(username=username, password=password)


async def get_information():
    print("Logging in...")
    await client.login()

    print("Retrieving cars...")
    # Returns cars registered to your account + information about each car.
    cars = await client.get_vehicles()

    for car in cars:
        await car.update()

        # Dump all the information collected so far
        pp.pprint(car._dump_all())

        # Alias
        print(f"Alias: {car.alias}")
        # Set alis
        # await car.set_alias("RAV4")

        ## Basic information
        # mileage = car.dashboard.odometer
        # print(f"Mileage : {mileage}")
        ## Or retrieve the energy level (electric or gasoline)
        # fuel = car.dashboard.fuel_level
        # print(f"Fuel    : {fuel}")
        # battery = car.dashboard.battery_level
        # print(f"Battery : {battery}")
        ## Or Parking information:
        # latitude = car.location.latitude
        # print(f"Latitude : {latitude}")

        ## Notifications => True retrieve all, False just unread
        # notifications = car.notifications(True)[:5]
        # if notifications:
        #    print("Notifications:")
        #    for notification in notifications:
        #        print(f"    {notification.date} : {notification.message}")


loop = asyncio.get_event_loop()
loop.run_until_complete(get_information())
loop.close()
