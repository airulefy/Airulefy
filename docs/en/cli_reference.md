# CLI Reference

Airulefy can be operated through a command-line interface (CLI). This page describes all available commands and options.

## Basic Usage

```bash
airulefy [options] [command]
```

## Global Options

| Option | Description |
|--------|-------------|
| `--version` | Show version information and exit |
| `--help` | Show help message and exit |

## Commands

### generate

Generate AI rule files.

```bash
airulefy generate [options]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--copy`, `-c` | Force copy mode instead of symlink |
| `--verbose`, `-v` | Show detailed output |
| `--preserve-structure`, `-p` | Preserve directory structure and output multiple .mdc files for Cursor |
| `--help` | Show help message |

**Examples:**

```bash
# Generate rules using the default mode (as defined in configuration)
airulefy generate

# Generate rules using copy mode
airulefy generate --copy

# Generate rules with detailed output
airulefy generate --verbose

# Generate rules preserving directory structure for Cursor
airulefy generate --preserve-structure
```

### watch

Watch the `.ai/` directory for changes and automatically regenerate rule files.

```bash
airulefy watch [options]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--copy`, `-c` | Force copy mode instead of symlink |
| `--preserve-structure`, `-p` | Preserve directory structure and output multiple .mdc files for Cursor |
| `--help` | Show help message |

**Examples:**

```bash
# Watch for changes using default mode
airulefy watch

# Watch for changes using copy mode
airulefy watch --copy

# Watch for changes preserving directory structure for Cursor
airulefy watch --preserve-structure
```

### validate

Validate the configuration and rule files.

```bash
airulefy validate
```

**Options:**

| Option | Description |
|--------|-------------|
| `--help` | Show help message |

**Examples:**

```bash
airulefy validate
```

### list-tools

List supported AI tools and their configurations.

```bash
airulefy list-tools
```

**Options:**

| Option | Description |
|--------|-------------|
| `--help` | Show help message |

**Examples:**

```bash
airulefy list-tools
```

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | Error/Failure |
