# **CLI Tool Implementation Guide (Minimum Viable Product)**

## **Overview**

This guide explains how to implement a modular Python CLI tool that supports dynamic command sets. The tool can be extended by installing additional command sets via `pip`, and it includes a basic set of commands out of the box.

## **Directory Structure**

The directory structure should resemble the following:

```
cli_tool/
├── cli_tool/
│   ├── __init__.py
│   ├── basic_commands.py
│   ├── cli.py
│   ├── loader.py
├── docs/
│   ├── index.md
│   ├── mvp.md
│   ├── objective.md
├── .gitignore
├── pyproject.toml
├── README.md
├── requirements.txt (optional)
└── setup.py
```

### **File Descriptions**

-   `cli_tool/cli.py`: The main CLI application logic and loop.
-   `cli_tool/loader.py`: Responsible for dynamically loading command sets.
-   `setup.py`: Defines package configuration and entry points.
-   `README.md`: Describes the CLI tool and its functionality.

---

## **Step-by-Step Implementation**

### **Step 1: Create the `cli_tool/cli.py` File**

This file will contain the main application logic, including the CLI loop that listens for commands.

1. **Define the `CLIApp` class**:
   The class manages the command loop and handles user input.

```python
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
```

-   **`__init__`**: Initializes an empty dictionary (`self.commands`) to store available commands.
-   **`run`**: Runs the command loop, processes commands, and shows the available ones. Commands are dynamically loaded by calling `load_commands(self)`.

### **Step 2: Create the `cli_tool/loader.py` File**

This file will contain logic for dynamically loading command sets based on installed packages.

1. **Define the `load_commands` function**:

```python
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
```

-   **`pkg_resources.iter_entry_points("cli_app.commands")`**: This iterates over all installed packages that provide command sets. It loads them dynamically into the `commands` dictionary of `cli_app`.

### **Step 3: Create the `setup.py` for Package Configuration**

This file will define the package’s metadata and its entry points for CLI commands.

1. **Set up the `setup.py` file**:

```python
# setup.py

from setuptools import setup, find_packages

setup(
    name="atari_monk_cli_tool",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cli_tool = cli_tool.cli:main",
        ],
        "cli_tool.commands": [  # Register the "cli_tool.commands" entry point group
            "basic_commands = cli_tool.basic_commands:load",  # Register the basic command set
        ],
    },
    install_requires=[],
    description="A modular CLI application that supports dynamic command sets.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="atari monk",
    author_email="atari.monk1@gmail.com",
    url="https://github.com/atari-monk/cli_tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.12.0",
)
```

-   **`entry_points`**: Defines two entry points:
    -   `console_scripts`: This creates a command line tool named `cli_tool`, which will run the `main` function in `cli.py`.
    -   `cli_app.commands`: This is where the command sets are registered. The basic command set is defined as `basic_commands` and is loaded from the `cli_tool.basic_commands:load` function.

### **Step 4: Create the Basic Command Set**

Create a `basic_commands` module that will provide a default set of commands.

1. **Create a `cli_tool/basic_commands.py` file**:

```python
# basic_commands.py

def load():
    print("basic_commands.load() called")
    def hello():
        print("Hello, CLI World!")

    return {
        "hello": hello
    }
```

-   **`load()`**: Returns a dictionary with the available commands (`hello` and `exit`), each associated with its corresponding function.

### **Step 5: Test the CLI Tool**

After setting up your package, you can test it:

1. **Install the CLI tool** locally by running:

    ```bash
    pip install .
    ```

2. **Run the CLI tool** by typing:

    ```bash
    cli_tool
    ```

3. You should be able to interact with the CLI, and it will list available commands such as `hello` and `exit`.

### **Step 6: Add Additional Command Sets**

To add new command sets, follow these steps:

1. **Create a new package** for your custom commands. For example, create `command_sets/custom_commands.py`.
2. **In the `setup.py`** of that package, register the new commands in the `cli_app.commands` entry point:

    ```python
    entry_points={
        "cli_app.commands": [
            "custom_commands = command_sets.custom_commands:load",
        ],
    }
    ```

3. **Install the new command set** via pip:

    ```bash
    pip install command_sets
    ```

    The new commands will be loaded and available in the main `cli_tool`.

---

## **Update `setup.py` to Use `pyproject.toml`**

1. **Create a `pyproject.toml`**:
   In the root of your project, add a file named `pyproject.toml`:

    ```toml
    [build-system]
    requires = ["setuptools>=64", "wheel"]
    build-backend = "setuptools.build_meta"
    ```

2. **Update Installation Command**:
   Install your package with the `--use-pep517` flag:

    ```bash
    pip install -e . --use-pep517
    ```

    This uses the modern PEP 517 build backend.

## **Commands**

### Differences Between `pip install .` and `pip install -e .`

| Command            | Behavior                                                                                             |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| `pip install .`    | Installs the package non-editably. Code changes in the source folder do not affect the installation. |
| `pip install -e .` | Installs the package in **editable** mode. Code changes in the source folder immediately reflect.    |

---

### Which One Should You Use?

1. **For Development**:
   Use `pip install -e .` so your changes reflect immediately without needing to reinstall.

2. **For Deployment**:
   Use `pip install .` to install a finalized version of the package as a regular, non-editable install.

---

### Run app in terminal

```bash
python -m cli_tool.cli
```

## **Conclusion**

This guide has walked you through the steps needed to create a dynamic and extensible Python CLI tool. The CLI tool supports loading and installing command sets from packages, allowing you to extend its functionality easily.

-   **Basic setup**: You have created the core logic to handle commands and load them dynamically from installed packages.
-   **Modular command sets**: By leveraging entry points, you can extend the CLI tool with additional command sets that can be installed independently.
