# basic_commands.py

import os
from cli_tool.config import LOGGER_CONFIG
from cli_logger.logger import setup_logger

logger = setup_logger(__name__, LOGGER_CONFIG)

def load():
    logger.debug("basic_commands.load() called")

    def clear(_):
        logger.info("Clearing terminal screen...")
        os.system('cls' if os.name == 'nt' else 'clear')

    return {
        "clear": clear
    }
