import pkg_resources

def load_commands(self):
        """Load commands from installed packages using entry points."""
        for entry_point in pkg_resources.iter_entry_points("cli_app.commands"):
            try:
                command_module = entry_point.load()
                self.commands[entry_point.name] = command_module
            except Exception as e:
                print(f"Error loading command {entry_point.name}: {e}")
