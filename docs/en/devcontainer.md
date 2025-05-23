# DevContainer

Airulefy supports Visual Studio Code's DevContainer feature, allowing you to easily set up a development environment. This page explains how to configure and use DevContainers with Airulefy.

## What is a DevContainer?

A DevContainer is a VS Code feature that allows you to create a complete development environment within a Docker container. This ensures that every developer can work in the same consistent environment with identical settings, tools, and extensions.

## Airulefy's Development Environment

The Airulefy project provides a DevContainer configuration with the following features:

- Python 3.11 environment
- Poetry for Python package management
- Automatic test running
- Pre-installed code quality tools (black, isort, mypy)
- Automatic configuration of VS Code Python extensions

## devcontainer.json

The `.devcontainer/devcontainer.json` file is the main configuration file for the DevContainer. Here's an example configuration used in Airulefy:

```json
{
    "name": "Airulefy Development",
    "dockerFile": "Dockerfile",
    "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "python.linting.enabled": true,
        "python.linting.pylintEnabled": false,
        "python.linting.mypyEnabled": true,
        "python.formatting.provider": "black",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "njpwerner.autodocstring"
    ],
    "postCreateCommand": "poetry install && pre-commit install",
    "remoteUser": "vscode"
}
```

## Dockerfile

The `.devcontainer/Dockerfile` defines the base image and additional setup steps for the DevContainer:

```Dockerfile
FROM mcr.microsoft.com/devcontainers/python:3.11

# Poetry environment variables
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version

# Install necessary system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspaces/Airulefy
```

## Automatic Test Running

The Airulefy development environment is configured to automatically run tests in the background. This is set up in `.vscode/settings.json` as follows:

```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.testing.autoTestDiscoverOnSaveEnabled": true
}
```

This will automatically run relevant tests whenever you save a file.

## Using the Development Container

1. Install Visual Studio Code and the [Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. Clone the Airulefy repository:
   ```bash
   git clone https://github.com/airulefy/Airulefy.git
   cd Airulefy
   ```

3. Open the folder in VS Code:
   ```bash
   code .
   ```

4. VS Code will detect the `.devcontainer` folder and show a notification; select "Reopen in Container"

5. Wait for the container to build and configure (this may take a few minutes the first time)

6. You're now ready to start developing Airulefy in a fully configured environment!

## Troubleshooting

### Rebuilding the Container

If dependencies change or you need to rebuild the container for any reason:

1. Open the VS Code command palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Select "Remote-Containers: Rebuild Container"

### Port Forwarding

To access services running inside the container, use port forwarding.
VS Code will automatically detect many ports, but you can add them manually:

1. Open the VS Code command palette
2. Select "Remote-Containers: Forward Port from Container"
3. Enter the port number you want to forward
