![GitHub Workflow](https://img.shields.io/github/actions/workflow/status/pytoyoda/pytoyoda/build.yml)
![Codecov](https://img.shields.io/codecov/c/github/pytoyoda/pytoyoda)
![Commit activity](https://img.shields.io/github/commit-activity/y/pytoyoda/pytoyoda)
![GitHub Release](https://img.shields.io/github/release/pytoyoda/pytoyoda.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pytoyoda)

# Toyota Connected Services Europe Python module

<b><p align=center> 🚨 Breaking changes ahead 🚨 </p></b>

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
pip install pytoyoda
```

## Usage

For a quick start on how to use the package take a look at the `simple_client_example.py` file contained in the report. You can also use and execute this file directly by using the following commands:

```bash
python -m venv pytoyoda
source pytoyoda/bin/activate
python -m pip install "pytoyoda@git+https://github.com/pytoyoda/pytoyoda@main"
curl -LO https://raw.githubusercontent.com/pytoyoda/pytoyoda/main/simple_client_example.py
# Create a credentials.json file with {"username":"your@mail.tld","password":"yourpassword"}
python simple_client_example.py
```

## Known issues

- Statistical endpoint will return `None` if no trip have been performed in the requested timeframe. This problem will often happen at the start of each week, month or year. Also daily stats will of course also be unavailable if no trip have been performed.
- Currently, it is only possible to get various vehicle information. Functions for controlling and setting vehicle properties have not yet been implemented.

## Docs

Coming soon...

## Contributing

This python module uses poetry (>= 2.0.0) and pre-commit.

To start contributing, fork this repository and run `poetry install`. Then create a new branch. Before making a PR, please run pre-commit `poetry run pre-commit run --all-files` and make sure that all tests passes locally first by running `pytest tests/`.

## Note

As I [@DurgNomis-drol](https://github.com/DurgNomis-drol) am not a professional programmer. I will try to maintain it as best as I can. If someone is interested in helping with this, they are more the welcome to message me to be a collaborator on this project.

## Credits

A huge thanks go to [@calmjm](https://github.com/calmjm) for making [tojota](https://github.com/calmjm/tojota).
