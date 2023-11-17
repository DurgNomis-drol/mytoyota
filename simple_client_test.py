import json
import asyncio
from mytoyota.client import MyT

#username = "user@nowhere.special"
#password = "<password>"

username = "somebody@someplace.overthere"
password = "password"
brand = "T"  # or lexus

# Get supported regions, can be passed to the optional 'region' argument of MyT
# At this moment, only the 'europe' region is supported
print(MyT.get_supported_regions())

client = MyT(username=username, password=password, brand=brand)

async def get_information():
    print("Logging in...")
    await client.login()

    print("Retrieving cars...")
    # Returns cars registered to your account + information about each car.
    cars = await client.get_vehicles()

    for car in cars:
        # Returns live data from car/last time you used it as an object.
        vehicle = await client.get_vehicle_status(car)

        # Dump all the information collected so far
        vehicle._dump_all()

        # You can either get them all async (Recommended) or sync (Look further down).
        #data = await asyncio.gather(
        #    *[
        #        client.get_driving_statistics(vehicle.vin, interval="day"),
        #        client.get_driving_statistics(vehicle.vin, interval="isoweek"),
        #        client.get_driving_statistics(vehicle.vin),
        #        client.get_driving_statistics(vehicle.vin, interval="year"),
        #    ]
        #)

        # You can access odometer data like this:
        mileage = vehicle.dashboard.odometer
        print(f"Mileage : {mileage}")
        # Or retrieve the energy level (electric or gasoline)
        fuel = vehicle.dashboard.fuel_level
        print(f"Fuel    : {fuel}")
        battery = vehicle.dashboard.battery_level
        print(f"Battery : {battery}")
        # Or Parking information:
        latitude = vehicle.parkinglocation.latitude
        print(f"Latitude : {latitude}")

        # Daily stats
        #daily_stats = await client.get_driving_statistics(vehicle.vin, interval="day")

        # ISO 8601 week stats
        #iso_weekly_stats = await client.get_driving_statistics(vehicle.vin, interval="isoweek")

        # Monthly stats is returned by default
        #monthly_stats = await client.get_driving_statistics(vehicle.vin)

        # Get year to date stats.
        #yearly_stats = await client.get_driving_statistics(vehicle.vin, interval="year")


loop = asyncio.get_event_loop()
loop.run_until_complete(get_information())
loop.close()