# Contributing

Thank you for your interest in contributing to the Airulefy project! This guide explains how to set up your development environment, create pull requests, and follow coding conventions.

## Development Environment Setup

### Requirements

- Python 3.11 or higher
- Poetry (for package management)
- Git

### Setup Steps

1. Clone the repository:

```bash
git clone https://github.com/airulefy/Airulefy.git
cd Airulefy
```

2. Install dependencies with Poetry:

```bash
# If you don't have Poetry installed yet
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

3. Install pre-commit hooks:

```bash
poetry run pre-commit install
```

### Using DevContainer

If you're using VS Code with extensions, you can easily set up a development environment with DevContainer:

1. After cloning the repository, open it in VS Code:

```bash
git clone https://github.com/airulefy/Airulefy.git
code Airulefy
```

2. When VS Code detects the `.devcontainer` folder, select "Reopen in Container".

See the [DevContainer documentation](./devcontainer.md) for more details.

## Development Workflow

### Branch Strategy

- `main`: Released code
- `develop`: Code in development
- Feature branches: `feature/xxxx`
- Bug fix branches: `fix/xxxx`

### Adding a Feature or Fixing a Bug

1. Create a new branch from the latest `develop`:

```bash
git checkout develop
git pull
git checkout -b feature/your-feature-name
```

2. Implement your changes.

3. Add or update tests and ensure all tests pass:

```bash
poetry run pytest
```

4. Format your code and run linters:

```bash
poetry run black .
poetry run isort .
poetry run mypy .
```

5. Commit your changes (using [Conventional Commits](#conventional-commits) format):

```bash
git add .
git commit -m "feat: add new feature X"
```

6. Push your changes:

```bash
git push -u origin feature/your-feature-name
```

7. Create a pull request on GitHub, targeting the `develop` branch.

## Testing

Airulefy uses pytest for running tests:

```bash
# Run all tests
poetry run pytest

# Generate coverage report
poetry run pytest --cov=airulefy

# Run specific test file
poetry run pytest tests/test_cli.py
```

Make sure to add corresponding tests for new features and update tests when modifying existing functionality.

## Coding Conventions

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/) for automatic formatting
- Use [mypy](http://mypy-lang.org/) for type checking

### Documentation

- Add docstrings to all public functions, classes, and methods
- Use [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

### <a name="conventional-commits"></a>Conventional Commits

Commit messages should follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types include:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation-only changes
- `style`: Changes that don't affect code meaning (whitespace, formatting, missing semi-colons, etc)
- `refactor`: Code changes that neither fix a bug nor add a feature
- `perf`: Code changes that improve performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries

Example:

```
feat: add auto-reconnect feature to watch mode

Connection now attempts to automatically reconnect every 30 seconds if disconnected.
This improves reliability during long-running operations.

Fixes #123
```

## Pull Requests

Before submitting a pull request:

1. Ensure your code passes all tests
2. Ensure your code is properly formatted
3. Update documentation as needed
4. Include a detailed description of your changes in the pull request

## Release Process

Airulefy releases follow these steps:

1. Ensure all tests pass on the `develop` branch
2. Update version number (in `pyproject.toml`)
3. Update CHANGELOG
4. Merge to `main` branch
5. Create a release tag
6. Publish to PyPI

## Questions?

If you have questions or concerns, please create a new issue in the GitHub Issues section.
We'll respond as soon as possible.

We look forward to your contributions!
