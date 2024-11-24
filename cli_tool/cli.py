# cli.py

import os
from cli_tool.loader import load_commands
from cli_tool.config import LOGGER_CONFIG
from cli_logger.logger import setup_logger    

logger = setup_logger(__name__, LOGGER_CONFIG)

class CLIApp:
    def __init__(self):
        self.commands = {}
        load_commands(self.commands)

    def run(self):
        logger.info("Welcome to CLI App! Type 'help' for available commands.")
        logger.info(f"Current working directory: {os.getcwd()}")

        while True:
            user_input = input("cli_tool> ").strip()
            if not user_input:
                continue
            if user_input == "exit":
                break
            elif user_input == "help":
                logger.info(f"Available commands: {', '.join(self.commands.keys())}")
            else:
                parts = user_input.split(maxsplit=1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else ""

                if command in self.commands:
                    try:
                        self.commands[command](args)
                    except Exception as e:
                        logger.error(f"Error running command {command}: {e}")
                else:
                    logger.warning("Unknown command. Type 'help' to see available commands.")

def main():
    CLIApp().run()

if __name__ == "__main__":
    main()
