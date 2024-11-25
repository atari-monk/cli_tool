# cli.py

import os
from cli_logger.logger import setup_logger
from cli_tool.config import LOGGER_CONFIG
from cli_tool.loader import load_commands
from keyval_storage.config_provider import ConfigProvider, PathData
from keyval_storage.storage_provider import StorageProvider, StorageConfig

logger = setup_logger(__name__, LOGGER_CONFIG)

STORAGE_PATH_KEY = 'storage_path'

class CLIApp:
    def __init__(self):
        self._commands = {}
        load_commands(self._commands)
        self._configProvider = ConfigProvider(PathData('C:\cli_tool', 'config.json'))
        self._storageProvider = StorageProvider(StorageConfig('storage_path', 'storage.json'))

    def run(self):
        logger.info("Welcome to CLI App! Type 'help' for available commands.")
        logger.info(f"Current working directory: {os.getcwd()}")

        config = self._configProvider.load_file()
        if config:
            _ = self._storageProvider.load_storage(config[STORAGE_PATH_KEY])
        else:
            _, storageFilePath = self._storageProvider.save_storage()
            self._configProvider.save_file({STORAGE_PATH_KEY: storageFilePath})

        while True:
            user_input = input("cli_tool> ").strip()
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
    CLIApp().run()

if __name__ == "__main__":
    main()
