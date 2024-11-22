# basic_commands.py

def load():
    print("basic_commands.load() called")
    def hello():
        print("Hello, CLI World!")

    return {
        "hello": hello
    }
