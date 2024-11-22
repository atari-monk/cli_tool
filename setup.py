from setuptools import setup, find_packages

setup(
    name="atari_monk_cli_tool",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cli_tool = cli_tool.cli:main",
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
    python_requires=">=3.13.0",
)
