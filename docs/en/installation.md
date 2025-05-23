# Installation

Airulefy can be installed in various ways. Choose the method that fits your environment and preferences.

## Prerequisites

- Python 3.11 or higher
- pip or Poetry (recommended)

## Installation with Poetry (Recommended)

[Poetry](https://python-poetry.org/) is a modern Python package manager that makes dependency management and environment isolation easier.

```bash
# If you don't have Poetry installed yet
curl -sSL https://install.python-poetry.org | python3 -

# Install Airulefy
poetry add airulefy
```

To install as a development dependency for an existing project:

```bash
poetry add --dev airulefy
```

## Installation with pip

Install using the standard Python package manager:

```bash
pip install airulefy
```

To install a specific version:

```bash
pip install airulefy==0.1.0
```

## DevContainer Setup

If you're using VS Code's DevContainer, you can easily set up the environment:

1. Add the following to your `.devcontainer/devcontainer.json` file:

```json
{
  "name": "Python Development",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "postCreateCommand": "pip install airulefy",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python"
      ]
    }
  }
}
```

2. Restart your DevContainer, and Airulefy will be automatically installed.

## Using with GitHub Codespaces

When using GitHub Codespaces:

1. Include the DevContainer configuration in your repository (see above)
2. When you launch Codespaces, Airulefy will be automatically installed
3. Alternatively, you can install directly in the Codespaces terminal:

```bash
pip install airulefy
```
