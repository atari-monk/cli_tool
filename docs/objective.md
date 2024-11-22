# Objective/Requirements: CLI Application with Extensible Command Sets

Python CLI tool with the following requirements:

1. **CLI Loop with Commands and Help**:

    - The tool should run in a loop, allowing the user to enter commands.
    - It should also provide help on commands (e.g., `--help` or `-h`).

2. **Installable by Package**:

    - The tool should be installable via `pip` (e.g., `pip install cli_tool`).

3. **Dynamic Loading of Command Sets**:

    - The CLI tool should be able to dynamically load commands from a folder within a package.
    - Command sets are separate packages that can be installed individually (e.g., `pip install command_set_name`).
    - The tool should load the corresponding command set by detecting installed packages.

4. **Include Basic Commands Package**:

    - When the `cli_tool` package is installed, it should automatically install a basic set of commands (i.e., a `basic_commands` package).
    - This ensures that certain core commands are available out of the box.

5. **Support for Installing Additional Command Sets**:
    - Separate command sets can be installed as additional packages (e.g., `pip install command_set_name`).
    - Each set can provide a specific set of commands, and they should be loaded into the tool when needed.

---
