# basic_commands.py

from cli_tool.config import LOGGER_CONFIG
from cli_tool.logger import setup_logger

logger = setup_logger(__name__, LOGGER_CONFIG)

def load():
    logger.debug("basic_commands.load() called")

    def hello(args):
        logger.info(f"Hello, CLI World! Args received: {args}")

    return {
        "hello": hello
    }
