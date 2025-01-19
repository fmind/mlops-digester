"""Define global context for the application."""

# %% IMPORTS

import sys

import logfire
from loguru import logger

from mlops_digester import settings

# %% SERVICES


def configure_loguru(loguru_settings: settings.LoguruServiceSettings) -> None:
    """Configure the loguru service from settings."""
    logger.remove()  # remove previous logger instances
    logger_config = loguru_settings.model_dump()
    logger.add(sink=sys.stderr, **logger_config)


def configure_logfire(logfire_settings: settings.LogfireServiceSettings) -> None:
    """Configure the logfire service from settings."""
    logfire_config = logfire_settings.model_dump()
    logfire.configure(**logfire_config)
