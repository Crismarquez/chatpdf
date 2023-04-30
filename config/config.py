import os
from pathlib import Path
import sys
import logging
import logging.config
from rich.logging import RichHandler
from dotenv import dotenv_values


BASE_DIR = Path(__file__).parent.parent.absolute()
CONFIG_DIR = Path(BASE_DIR, "config")
DATA_DIR = Path(BASE_DIR, "data")
PROEJECTS_DIR = Path(DATA_DIR, "projects")
STORE_DIR = Path(BASE_DIR, "store")
MODELS_DIR = Path(STORE_DIR, "models")
RESULTS_DIR = Path(BASE_DIR, "results")
DATARESEARCH_DIR = Path(BASE_DIR, "data_research")
LOGS_DIR = Path(BASE_DIR, "logs")


# Create dirs
DATA_DIR.mkdir(parents=True, exist_ok=True)
PROEJECTS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_FILES = {
    "ocr_show": "https://drive.google.com/drive/folders/1__EaMm_D4sZUj4dfXz_WnOAMHzFm3rkh?usp=share_link",
    "anual_report": "https://drive.google.com/drive/folders/1TZfU9ignpXB2FiNgQ0ci-F0oDmreHgzY?usp=share_link"
}

ENV_VARIABLES = {
    **dotenv_values(".env"),  # load environment variables from .env file
    **os.environ,  # override loaded values with environment variables
}

os.environ['OPENAI_API_KEY'] = ENV_VARIABLES['OPENAI_API_KEY']

# Logger
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "minimal": {"format": "%(message)s"},
        "detailed": {
            "format": "%(levelname)s %(asctime)s [%(name)s:%(filename)s:%(funcName)s:%(lineno)d]\n%(message)s\n"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "minimal",
            "level": logging.DEBUG,
        },
        "info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "info.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.INFO,
        },
        "error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "error.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.ERROR,
        },
    },
    "root": {
        "handlers": ["console", "info", "error"],
        "level": logging.INFO,
        "propagate": True,
    },
}

logging.config.dictConfig(logging_config)
logger = logging.getLogger()
logger.handlers[0] = RichHandler(markup=True)
