---
title: PDM
date: 2024-08-21
draft: false
---

## Create a New Project

Initialize a new project with a `pyproject.toml` file:

```shell
pdm init
```

## Project Structure

Assuming the project is named "hello," a typical PDM project structure with a `src` directory might look like this:

```shell
hello/
├── .pdm-python         # Automatically generated file (add to .gitignore)
├── pyproject.toml      # Project configuration file
├── pdm.lock            # Automatically generated lock file
├── src/                # Source code directory
│   └── hello/          # Main application package
│       ├── __init__.py # Marks the directory as a package
│       └── main.py     # Entry point of the application
└── tests/              # Test directory
    ├── __init__.py     # Marks the directory as a package
    └── test_main.py    # Example test file
```

## Manage Packages

Add and install a regular (runtime) dependency to your project:

```shell
pdm add <package_name>
```

Add and install a development dependency:

```shell
pdm add -d <package_name>
```

This will add the development dependency to the `dev` group under `[tool.pdm.dev-dependencies]` in your `pyproject.toml`.

## Using `pdm run`

Run the `main.py` script:

```shell
pdm run python src/hello/main.py
```

Run a script defined in `pyproject.toml`:

```shell
pdm run <script_name>
```

## Using `pdm run` with Pytest

Run tests in the "hello" project:

```shell
pdm run pytest
```

Run a specific test module or function:

```shell
pdm run pytest tests/test_main.py
```

## Example Test with Pytest

Assume you have a `greet` function defined in the `hello` module within the `src/hello/` directory.

`src/hello/main.py`:

```shell
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

`tests/test_main.py`:

```shell
import pytest
from hello.main import greet

def test_greet():
    assert greet("World") == "Hello, World!"
```

## Manage Virtual Environments

Create and activate a virtual environment automatically managed by PDM:

```shell
pdm venv create
pdm venv activate
```

Deactivate the virtual environment:

```shell
deactivate
```

## Requirements Management

### Example `pyproject.toml`

Here’s how your `pyproject.toml` file might look for the "hello" project:

```shell
[project]
name = "hello"
version = "0.1.0"
description = "Default template for PDM package"
authors = [
    {name = "Kyle Kestell", email = "kyle@kestell.org"},
]
requires-python = ">=3.12"
readme = "README.md"
license = { text = "MIT" }
dependencies = [
    "rich>=13.7.1",
]

[tool.pdm.dev-dependencies]
dev = [
    "pytest>=8.3.2",
]

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"

[tool.pdm]
distribution = true
```

### Export Regular and Development Dependencies

#### Export Regular (Runtime) Dependencies

To export only the regular (runtime) dependencies:

```shell
pdm export --without-hashes --prod > requirements.txt
```

#### Export Development Dependencies

To export the development dependencies:

```shell
pdm export --without-hashes --dev > requirements-dev.txt
```

### Install Dependencies from a Requirements File

Install dependencies from a requirements file:

```shell
pdm install -r requirements.txt
```

## Upgrade PDM

Upgrade PDM itself:

```shell
pdm self update
```
