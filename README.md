# Toyota Connected Services Python module

### [!] **This has not been published to PyPi yet**

## Description

Python 3 package to communicate with Toyota Connected Services.

## Installation

This package can be installed through `pip`.

```text
pip install mytoyota
```

## Usage

```python
import aiohttp
import asyncio
from mytoyota.client import MyT

username = "jane@doe.com"
password = "MyPassword"
locale = "da-dk"
session = aiohttp.ClientSession()

client = MyT(locale=locale, session=session)

print("Performing login...")
client.perform_login(username=username, password=password)

async def get_cars()
    print("Retrieving cars...")
    valid, cars = await client.get_cars()

    if valid:
        print(cars)
        return

loop = asyncio.get_event_loop()
loop.run_until_complete(get_cars())
loop.close()
```

### Get odometer information

```python
async def get_odometer(vin)
    print("Retrieving odometer information...")
    odometer, odometer_unit, fuel = await client.get_odometer(vin=vin)

    print(odometer)
    print(odometer_unit)
    print(fuel)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_odometer(vin))
loop.close()
```

### Get parking information

```python
async def get_parking(vin)
    print("Retrieving latest parking information...")
    parking = await client.get_parking(vin=vin)

    print(parking)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_parking(vin))
loop.close()
```

### Get vehicle information

```python
async def get_vehicle_info(vin)
    print("Retrieving vehicle information...")
    battery, hvac, last_updated = await client.get_vehicle_information(vin=vin)

    print(battery)
    print(hvac)
    print(last_updated)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_vehicle_info(vin))
loop.close()
```

## Contributing

This python uses poetry and pre-commit.

To start contributing, fork this repository and run `poetry install`. Then create a new branch. Before making a PR, please run pre-commit `poetry run pre-commit run --all-files` and make sure that all tests passes locally first.

## Note

As I [@DurgNomis-drol](https://github.com/DurgNomis-drol) is not a professional programmer. I will be maintain it as best as I can. If someone is interested in helping with this, they are more the welcome to message me to be a collaborator on this project.

## Credits

A huge thanks go to [@calmjm](https://github.com/calmjm) for making [tojota](https://github.com/calmjm/tojota). Which is used as the base for making this module.
