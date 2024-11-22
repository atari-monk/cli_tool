# loader.py

import pkg_resources

def load_commands(commands):
    """Load commands from installed packages using entry points."""
    for entry_point in pkg_resources.iter_entry_points("cli_tool.commands"):
        try:
            command_module = entry_point.load()  # Load the module (the load function)
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
