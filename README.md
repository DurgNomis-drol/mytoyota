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

### See [Documentation](https://github.com/DurgNomis-drol/mytoyota/documentation.md)

## Known issues

- Statistical endpoint will return `None` if no trip have been performed in the requested timeframe. This problem will often happen at the start of each week, month or year. Also daily stats will of course also be unavailable if no trip have been performed.

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
