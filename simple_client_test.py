import json
import asyncio
import pprint
from mytoyota.client import MyT


username = "somebody@someplace.overthere"
password = "password"
brand = "T"  # or lexus

pp = pprint.PrettyPrinter(indent=4)


client = MyT(username=username, password=password, brand=brand)

async def get_information():
    print("Logging in...")
    await client.login()

    print("Retrieving cars...")
    # Returns cars registered to your account + information about each car.
    cars = await client.get_vehicles()

    for car in cars:
        await car.update()

        # Dump all the information collected so far
        #pp.pprint(car._dump_all())

        print(f"Alias: {car.alias}")

        # This is not working something to do with incorrect headers!
        #await car.set_alias("My Car")

        # You can access odometer data like this:
        mileage = car.dashboard.odometer
        print(f"Mileage : {mileage}")
        # Or retrieve the energy level (electric or gasoline)
        fuel = car.dashboard.fuel_level
        print(f"Fuel    : {fuel}")
        battery = car.dashboard.battery_level
        print(f"Battery : {battery}")
        # Or Parking information:
        latitude = car.location.latitude
        print(f"Latitude : {latitude}")

loop = asyncio.get_event_loop()
loop.run_until_complete(get_information())
loop.close()