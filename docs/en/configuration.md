# Configuration

You can customize Airulefy's behavior through the `.ai-rules.yml` configuration file. 
This page describes all available configuration options and provides examples.

## Basic Configuration

Create a file named `.ai-rules.yml` in your project's root directory. Here's a basic example:

```yaml
default_mode: symlink
input_path: .ai
tools:
  cursor: {}
  cline: {}
  copilot: {}
  devin: {}
```

## Configuration Options

### Global Settings

| Option | Description | Default Value | Valid Values |
|--------|-------------|---------------|-------------|
| `default_mode` | Default synchronization mode | `symlink` | `symlink`, `copy` |
| `input_path` | Path to directory containing AI rule files | `.ai` | Any relative path |

### Tool-Specific Settings

Each tool can have the following options:

| Option | Description | Default Value | Valid Values |
|--------|-------------|---------------|-------------|
| `mode` | Synchronization mode for this tool | Value of `default_mode` | `symlink`, `copy` |
| `output` | Output file path | Tool-specific | Any relative path |

## Supported Tools and Default Outputs

| Tool Name | Default Output Path |
|-----------|---------------------|
| `cursor` | `.cursor/rules/core.mdc` |
| `cline` | `.cline-rules` |
| `copilot` | `.github/copilot-instructions.md` |
| `devin` | `devin-guidelines.md` |

## Configuration Examples

### Simple Configuration

```yaml
default_mode: symlink
```

Use symlinks for all tools with default output paths.

### Custom Output Paths

```yaml
default_mode: symlink
tools:
  cursor:
    output: ".cursor/rules/project-rules.mdc"
  devin:
    output: "docs/devin-instructions.md"
```

Customize the output paths for Cursor and Devin.

### Mixed Modes

```yaml
default_mode: symlink
tools:
  cursor: {}  # Use symlink
  cline:
    mode: copy  # Use copy
  copilot:
    mode: symlink  # Explicitly specify symlink
  devin:
    mode: copy  # Use copy
    output: "custom/path/devin-guide.md"  # Custom output path
```

Specify different synchronization modes and output paths for each tool.

### Custom Input Path

```yaml
default_mode: symlink
input_path: "docs/ai-rules"
```

Read AI rule files from `docs/ai-rules` directory instead of `.ai`.

## Notes

- `symlink` mode may require administrator privileges on Windows
- In environments where symlinks are not supported, `copy` mode is automatically used
- Output directories are automatically created if the file doesn't exist
