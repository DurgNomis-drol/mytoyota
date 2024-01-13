"""Load a central config for logging."""
import logging
import logging.config
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).parent

with open(file=BASE_DIR / "log_config.yaml", mode="r", encoding="utf-8") as config:
    config_dict = yaml.safe_load(config)

logging.config.dictConfig(config_dict)
