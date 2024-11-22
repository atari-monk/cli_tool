from cli_tool.loader import load_commands

class CLIApp:
    def __init__(self):
        self.commands = {}

    def run(self):
        """Main command loop."""
        load_commands()
        print("Welcome to CLI App! Type 'help' for available commands.")
        while True:
            command = input("cli_app> ").strip()
            if command == "exit":
                break
            elif command == "help":
                print("Available commands:", ", ".join(self.commands.keys()))
            elif command in self.commands:
                try:
                    self.commands[command]()
                except Exception as e:
                    print(f"Error running command {command}: {e}")
            else:
                print("Unknown command. Type 'help' to see available commands.")

def main():
    CLIApp().run()

if __name__ == "__main__":
    main()
