# Simple Args

To handle commands with arguments while keeping the loader and commands simple, you can enhance the `CLIApp` class to parse user input and pass arguments to the command functions. Here's a revised version of your code:

### Updated `cli.py`

```python
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
```

---

### Updated `basic_commands.py`

Update the `hello` function to accept arguments:

```python
def load():
    print("basic_commands.load() called")

    def hello(args):
        print(f"Hello, CLI World! Args received: {args}")

    return {
        "hello": hello
    }
```

---

### Explanation of Changes

1. **Command Parsing**:

    - The `user_input` is split into the command (`parts[0]`) and the arguments (`parts[1]` if it exists).
    - This keeps the core CLI logic simple and reusable.

2. **Passing Arguments**:

    - The command function is called with `args`. If no arguments are provided, an empty string is passed.

3. **Command Functions**:

    - Each command can decide how to handle the arguments (e.g., split further, validate, or process directly).

4. **Loader Unchanged**:
    - The `loader.py` remains untouched since the `commands` dictionary now expects functions that accept a single `args` parameter.

---

### Example Usage

1. Run the CLI:

    ```bash
    python cli.py
    ```

2. Execute commands:

    ```text
    cli_app> hello
    Hello, CLI World! Args received:

    cli_app> hello foo bar
    Hello, CLI World! Args received: foo bar
    ```

This approach keeps your loader and commands flexible while adding argument support in a straightforward manner.
