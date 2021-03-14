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
from mytoyota import MyT

username = "jane@doe.com"
password = "MyPassword"
locale = "da-dk"
session = aiohttp.ClientSession()

client = MyT(locale=locale, session=session)

print("Performing login...")
client.perform_login(username=username, password=password)

print("Retrieving cars...")
valid, cars = await client.get_cars()

if valid:
    print(cars)
else:
    print("Cannot find any car(s) connected to your account.")
```

### Get odometer information

```python
vin = "VINNUMBER"

odometer, odometer_unit, fuel = await client.get_odometer(vin=vin)

print(odometer)
print(odometer_unit)
print(fuel)
```

### Get parking information

```python
vin = "VINNUMBER"

parking = await client.get_parking(vin=vin)

print(parking)
```

### Get vehicle information

```python
vin = "VINNUMBER"

battery, hvac, last_updated = await client.get_vehicle_information(vin=vin)

print(battery)
print(hvac)
print(last_updated)
```

## Contributing
This python uses poetry and pre-commit. 

To start contributing, fork this repository and run `poetry install`. Then create a new branch. Before making a PR, please run pre-commit `poetry run pre-commit run --all-files` and make sure that all tests passes locally first.

## Note:
As I [@DurgNomis-drol] is not a professional programmer. I will be maintain it as best as I can. If someone is interested in helping with this, they are more the welcome to message me to be a collaborator on this project.