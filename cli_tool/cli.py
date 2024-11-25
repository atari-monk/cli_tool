# cli.py

import os
from cli_logger.logger import setup_logger
from cli_tool.config import LOGGER_CONFIG
from cli_tool.loader import load_commands
from keyval_storage.config_storage_interaction import ConfigStorageInteraction

logger = setup_logger(__name__, LOGGER_CONFIG)

APP_NAME = 'cli_tool'

class CliTool:
    def __init__(self):
        self._commands = {}
        load_commands(self._commands)
        self._configStorage = ConfigStorageInteraction(APP_NAME)

    def run(self):
        logger.info(f"Welcome to {APP_NAME}! Type 'help' for available commands.")
        logger.info(f"Current working directory: {os.getcwd()}")

        _ = self._configStorage.loadFromConfigOrCreate()

        while True:
            user_input = input(f"{APP_NAME}> ").strip()
            if not user_input:
                continue
            if user_input == "exit":
                break
            elif user_input == "help":
                logger.info(f"Available commands: {', '.join(self._commands.keys())}")
            else:
                parts = user_input.split(maxsplit=1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else ""

                if command in self._commands:
                    try:
                        self._commands[command](args)
                    except Exception as e:
                        logger.error(f"Error running command {command}: {e}")
                else:
                    logger.warning("Unknown command. Type 'help' to see available commands.")

def main():
    CliTool().run()

if __name__ == "__main__":
    main()
