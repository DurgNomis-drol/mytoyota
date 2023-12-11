[![GitHub Workflow Status][workflow-shield]][workflow]
[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]

# Toyota Connected Services Europe Python module

 <p align=center> 🚨 **Breaking changes ahead** 🚨 </p>
 <p align=center> Version 1.0.0 only supports the new ctpa-oneapi API endpoints that were introduced with the new MyToyota app. Some functions are not yet implemented and must first be determined due to the lack of API documentation. </p>
 <p align=center> Users of the old MyT app should use a mytoyota python module version < 1.0.0. </p>

⚠️ _This is still in beta_

⚠️ _Only EU is supported, other regions are not possible so far. See [this](https://github.com/widewing/toyota-na) for North America_

## Description

Python 3 package to communicate with [Toyota Connected Europe](https://www.toyota-europe.com/about-us/toyota-in-europe/toyota-connected-europe) Services.
This is an unofficial package and Toyota can change their API at any point without warning.

## Installation

This package can be installed through `pip`.

```text
pip install mytoyota
```

## Usage

```python
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
        pp.pprint(f"Dashboard: {car.dashboard}")
        # Location Information
        pp.pprint(f"Location: {car.location}")
        # Lock Status
        pp.pprint(f"Lock Status: {car.lock_status}")
        # Notifications
        pp.pprint(f"Notifications: {[[x] for x in car.notifications]}")

        # Dump all the information collected so far:
        # pp.pprint(car._dump_all())  # pylint: disable=W0212


loop = asyncio.get_event_loop()
loop.run_until_complete(get_information())
loop.close()
```

## Known issues

- tbd

## Docs

Coming soon...

## Contributing

This python module uses poetry (>= 1.5.1) and pre-commit.

To start contributing, fork this repository and run `poetry install`. Then create a new branch. Before making a PR, please run pre-commit `poetry run pre-commit run --all-files` and make sure that all tests passes locally first.

## Note

As I [@DurgNomis-drol](https://github.com/DurgNomis-drol) am not a professional programmer. I will try to maintain it as best as I can. If someone is interested in helping with this, they are more the welcome to message me to be a collaborator on this project.

## Credits

A huge thanks go to [@calmjm](https://github.com/calmjm) for making [tojota](https://github.com/calmjm/tojota).

[releases-shield]: https://img.shields.io/github/release/DurgNomis-drol/mytoyota.svg?style=for-the-badge
[releases]: https://github.com/DurgNomis-drol/mytoyota/releases
[workflow-shield]: https://img.shields.io/github/actions/workflow/status/DurgNomis-drol/mytoyota/build.yml?branch=master&style=for-the-badge
[workflow]: https://github.com/DurgNomis-drol/mytoyota/actions
[commits-shield]: https://img.shields.io/github/commit-activity/y/DurgNomis-drol/mytoyota.svg?style=for-the-badge
[commits]: https://github.com/DurgNomis-drol/mytoyota/commits/master
