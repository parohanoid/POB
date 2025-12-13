from setuptools import setup, find_packages

setup(
    name="parliament-of-bruce",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pob=parliament_of_bruce.cli:app",
        ],
    },
)
