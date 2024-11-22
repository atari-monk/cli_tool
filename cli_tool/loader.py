# loader.py

import importlib.metadata

def load_commands(commands):
    """Load commands from installed packages using modern entry points."""
    try:
        # Discover all entry points registered under "cli_tool.commands"
        entry_points = importlib.metadata.entry_points(group="cli_tool.commands")
        for entry_point in entry_points:
            try:
                # Load the `load` function or callable from the entry point
                command_module = entry_point.load()
                print(f"Loaded module: {entry_point.name} -> {command_module}")

                if callable(command_module):
                    # Call the `load` function to get the commands dictionary
                    loaded_commands = command_module()
                    print(f"Loaded commands: {loaded_commands}")
                    commands.update(loaded_commands)  # Merge into the main commands dictionary
                else:
                    print(f"Entry point {entry_point.name} did not return a callable")
            except Exception as e:
                print(f"Error loading command {entry_point.name}: {e}")
    except Exception as e:
        print(f"Error discovering entry points: {e}")
