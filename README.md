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
import arrow
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
        # Returns live data from car/last time you used it.
        vehicle = await client.get_vehicle_status(car)
        print(vehicle)

        # Stats returned in a dict
        daily_stats = await client.get_driving_statistics(cars[0]['vin'], interval="day")
        print(daily_stats)

        # Stats returned in json.
        weekly_stats = await client.get_driving_statistics_json(cars[0]['vin'], interval="week")
        print(weekly_stats)

        # Monthly stats is returned by default
        monthly_stats = await client.get_driving_statistics(cars[0]['vin'])
        print(monthly_stats)

        # Use the summary to get year to date stats.
        yearly_stats = await client.get_driving_statistics(car['vin'], interval="month", from_date=(arrow.now().floor("year").format("YYYY-MM-DD")))
        print(yearly_stats)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_information())
loop.close()

```

## Known issues

- Statistical endpoint will return "null" if no trip have been performed in the requested timeframe. This problem will often happen at the start of each week, month or year. Also daily stats will of course also be unavailable if no trip have been performed.
- Toyota's API can be a little flaky sometimes. So be aware of that when using this in your project.

## Docs

Coming soon...

## Contributing

This python module uses poetry and pre-commit.

To start contributing, fork this repository and run `poetry install`. Then create a new branch. Before making a PR, please run pre-commit `poetry run pre-commit run --all-files` and make sure that all tests passes locally first.

## Note

As I [@DurgNomis-drol](https://github.com/DurgNomis-drol) am not a professional programmer. I will try to maintain it as best as I can. If someone is interested in helping with this, they are more the welcome to message me to be a collaborator on this project.

## Credits

A huge thanks go to [@calmjm](https://github.com/calmjm) for making [tojota](https://github.com/calmjm/tojota).
