# Documentation

Some words about the documentation!

## Table of Contents

2. [Basic usage](#basic-usage)
   1. [Example](#example)
3. [Advanced usage](#advanced-usage)
   1. [Get supported regions](#get-supported-regions)
   2. [Get vehicle status](#get-vehicle-status)
   3. [Get driving statistics](#get-driving-statistic)
4. [Notes](#notes)

## Basic usage

### Example

This will return a list of vehicles connected to your account.

```python
import asyncio
from mytoyota.client import MyT

client = MyT(username="jane@doe.com", password="MyPassword", locale="da-dk", region="europe")

async def get_information():
    await client.login()

    cars = await client.get_vehicles()

    print(cars)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_information())
loop.close()
```

## Advanced usage

### Get supported regions

This will return a list with all the supported regions.

```python
print(MyT.get_supported_regions())
```

### Get vehicle status

Returns the corresponding vehicle with vehicle status as an object

Status includes:

- Alias, vin and details about the car
- Odometer data
- Location data
- Windows and lights data.

You can access data like this `vehicle.odometer.fuel` will get you the fuel state in percentage.

**Note:** Availability depends on model and year.

```python
import asyncio
from mytoyota.client import MyT

client = MyT(username="jane@doe.com", password="MyPassword", locale="da-dk", region="europe")

async def get_information():
    await client.login()

    cars = await client.get_vehicles()
    for car in cars:

        vehicle = await client.get_vehicle_status(car)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_information())
loop.close()
```

#### Return vehicles as json string

`cars = await client.get_vehicles_json()`

#### Return vehicle status as json string

`cars = await client.get_vehicle_status_json()`

### Get driving statistic

#### IMPORTANT!

No data will be provided if the start date of the current week, month or year is on the first of each.
Also if no trips have been performed in the time periode selected, not data will be returned.

#### Basic usage

`client.get_driving_statistics(vin="<vin-number>", interval=<interval>, from_date=<date>)`

| Arguments | Possiblities                                  |
| --------- | --------------------------------------------- |
| vin       | Vin number of the car                         |
| interval  | "day", "week", "isoweek", "month" or "year"   |
| from_date | From which date you want to return data from. |

**Note:** If the interval chosen is "isoweek", this cannot be older than 7 days from current date.

**Note:** If the interval chosen is "year", this cannot be older than the 01-01 of the current year.

```python
import asyncio
from mytoyota.client import MyT

client = MyT(username="jane@doe.com", password="MyPassword", locale="da-dk", region="europe")

async def get_information():
    await client.login()

    cars = await client.get_vehicles()
    for car in cars:

        vehicle = await client.get_vehicle_status(car)

        statistics = client.get_driving_statistics(vehicle.vin)

loop = asyncio.get_event_loop()
loop.run_until_complete(get_information())
loop.close()
```

The vehicle object have a holder for statistics, so it is easier to use the information later.

Just add this:

```python
vehicle.statistics.monthly = statistics
```

#### Gather statistics concurrently

```python
data = await asyncio.gather(
    *[
        client.get_driving_statistics(vehicle.vin, interval="day"),
        client.get_driving_statistics(vehicle.vin, interval="isoweek"),
        client.get_driving_statistics(vehicle.vin),
        client.get_driving_statistics(vehicle.vin, interval="year"),
    ]
)
```

## Notes
