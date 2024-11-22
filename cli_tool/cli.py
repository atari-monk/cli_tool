# cli.py

from cli_tool.loader import load_commands

class CLIApp:
    def __init__(self):
        self.commands = {}

    def run(self):
        """Main command loop."""
        load_commands(self.commands)
        print("Welcome to CLI App! Type 'help' for available commands.")
        while True:
            user_input = input("cli_app> ").strip()
            if not user_input:
                continue
            if user_input == "exit":
                break
            elif user_input == "help":
                print("Available commands:", ", ".join(self.commands.keys()))
            else:
                # Split command and arguments
                parts = user_input.split(maxsplit=1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else ""

                if command in self.commands:
                    try:
                        # Pass arguments to the command function
                        self.commands[command](args)
                    except Exception as e:
                        print(f"Error running command {command}: {e}")
                else:
                    print("Unknown command. Type 'help' to see available commands.")

def main():
    CLIApp().run()

if __name__ == "__main__":
    main()
