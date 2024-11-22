# basic_commands.py

def load():
    print("basic_commands.load() called")

    def hello(args):
        print(f"Hello, CLI World! Args received: {args}")

    return {
        "hello": hello
    }
