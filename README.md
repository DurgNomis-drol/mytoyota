[![GitHub Workflow Status][workflow-shield]][workflow]
[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]

# Toyota Connected Services Python module

### [!] **This is still in beta**

## Description

Python 3 package to communicate with Toyota Connected Services.
This is an unofficial package and Toyota can change their API at any point without warning.

## Installation

This package can be installed through `pip`.

```text
pip install mytoyota
```

## Usage

```python
import json
import asyncio
from mytoyota.client import MyT

username = "jane@doe.com"
password = "MyPassword"
locale = "da-dk"

# Get supported regions.
print(MyT.get_supported_regions())

client = MyT(username=username, password=password, locale=locale, region="europe")


async def get_information():
    print("Logging in...")
    await client.login()

    print("Retrieving cars...")
    # Returns cars registered to your account + information about each car.
    cars = await client.get_vehicles()

    for car in cars:

        # Returns live data from car/last time you used it as an object.
        vehicle = await client.get_vehicle_status(car)


        # You can either get them all async (Recommended) or sync (Look further down).
        data = await asyncio.gather(
            *[
                client.get_driving_statistics(vehicle.vin, interval="day"),
                client.get_driving_statistics(vehicle.vin, interval="isoweek"),
                client.get_driving_statistics(vehicle.vin),
                client.get_driving_statistics(vehicle.vin, interval="year"),
            ]
        )

        # You can deposit each result into premade object holder for statistics. This will make it easier to use in your code.

        vehicle.statistics.daily = data[0]
        vehicle.statistics.weekly = data[1]
        vehicle.statistics.monthly = data[2]
        vehicle.statistics.yearly = data[3]


        # You can access odometer data like this:
        fuel = vehicle.odometer.fuel
        # Or Parking information:
        latitude = vehicle.parking.latitude


        # Pretty print the object. This will provide you with all available information.
        print(json.dumps(vehicle.as_dict(), indent=3))


        # -------------------------------
        # All data is return in an object.
        # -------------------------------

        # Returns live data from car/last time you used it.
        vehicle = await client.get_vehicle_status(car)
        print(vehicle.as_dict())

        # Stats returned in a dict
        daily_stats = await client.get_driving_statistics(vehicle.vin, interval="day")
        print(daily_stats.as_list())

        # Stats returned in json.
        weekly_stats = await client.get_driving_statistics(vehicle.vin, interval="isoweek")
        print(weekly_stats.as_list())

        # ISO 8601 week stats
        iso_weekly_stats = await client.get_driving_statistics(vehicle.vin, interval="isoweek")
        print(iso_weekly_stats.as_list)

        # Monthly stats is returned by default
        monthly_stats = await client.get_driving_statistics(vehicle.vin)
        print(monthly_stats.as_list())

        #Get year to date stats.
        yearly_stats = await client.get_driving_statistics(vehicle.vin, interval="year")
        print(yearly_stats.as_list())


loop = asyncio.get_event_loop()
loop.run_until_complete(get_information())
loop.close()

```

## Known issues

- Statistical endpoint will return `None` if no trip have been performed in the requested timeframe. This problem will often happen at the start of each week, month or year. Also daily stats will of course also be unavailable if no trip have been performed.

## Docs

Coming soon...

## Contributing

This python module uses poetry and pre-commit.

To start contributing, fork this repository and run `poetry install`. Then create a new branch. Before making a PR, please run pre-commit `poetry run pre-commit run --all-files` and make sure that all tests passes locally first.

## Note

As I [@DurgNomis-drol](https://github.com/DurgNomis-drol) am not a professional programmer. I will try to maintain it as best as I can. If someone is interested in helping with this, they are more the welcome to message me to be a collaborator on this project.

## Credits

A huge thanks go to [@calmjm](https://github.com/calmjm) for making [tojota](https://github.com/calmjm/tojota).

[releases-shield]: https://img.shields.io/github/release/DurgNomis-drol/mytoyota.svg?style=for-the-badge
[releases]: https://github.com/DurgNomis-drol/mytoyota/releases
[workflow-shield]: https://img.shields.io/github/workflow/status/DurgNomis-drol/mytoyota/Linting?style=for-the-badge
[workflow]: https://github.com/DurgNomis-drol/mytoyota/actions
[commits-shield]: https://img.shields.io/github/commit-activity/y/DurgNomis-drol/mytoyota.svg?style=for-the-badge
[commits]: https://github.com/DurgNomis-drol/mytoyota/commits/master
