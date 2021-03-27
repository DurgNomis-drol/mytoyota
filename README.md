# Toyota Connected Services Python module

### [!] **This is still in beta**

## Description

Python 3 package to communicate with Toyota Connected Services.

## Installation

This package can be installed through `pip`.

```text
pip install mytoyota
```

## Usage

```python
import asyncio
from mytoyota.client import MyT

username = "jane@doe.com"
password = "MyPassword"
locale = "da-dk"

client = MyT(username=username, password=password, locale=locale, region="europe")


async def get_information():
    print("Logging in...")
    await client.login()

    print("Retrieving cars...")
    # Returns information about the cars registered to your account
    cars = await client.get_vehicles()

    print(await client.gather_all_information_json())

    statistics = await client.get_driving_statistics_from_date_json(cars[0]['vin'])

    print(statistics)

    statistics = await client.get_driving_statistics_from_week_json(cars[0]['vin'])

    print(statistics)

    statistics = await client.get_driving_statistics_from_month_json(cars[0]['vin'])

    print(statistics)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_information())
loop.close()

```

## Docs

Coming soon...

## Contributing

This python module uses poetry and pre-commit.

To start contributing, fork this repository and run `poetry install`. Then create a new branch. Before making a PR, please run pre-commit `poetry run pre-commit run --all-files` and make sure that all tests passes locally first.

## Note

As I [@DurgNomis-drol](https://github.com/DurgNomis-drol) is not a professional programmer. I will be maintain it as best as I can. If someone is interested in helping with this, they are more the welcome to message me to be a collaborator on this project.

## Credits

A huge thanks go to [@calmjm](https://github.com/calmjm) for making [tojota](https://github.com/calmjm/tojota).
