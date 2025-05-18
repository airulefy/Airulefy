# Airulefy

AI rule file generator and symlink manager for AI coding tools.

## Quickstart

1. Install the package:
```bash
pip install airulefy
```

2. Create your AI rules in `.ai/` directory:
```bash
mkdir .ai
echo "# My AI Rules" > .ai/instruction.md
```

3. Generate rule files:
```bash
airulefy generate
```

## Features

- Supports multiple AI coding tools:
  - Cursor
  - Cline
  - GitHub Copilot
  - Devin
- Automatic symlink/copy management
- Watch mode for real-time updates
- Shell script fallback
- Configuration via YAML

## Configuration

Create `.ai-rules.yml` in your project root:

```yaml
default_mode: symlink  # or copy
tools:
  cursor:
    output: ".cursor/rules/core.mdc"
  cline:
    mode: copy
```

## Philosophy

Airulefy aims to maintain a "single source of truth" for AI coding tool rules by:

1. Storing all rules in `.ai/` directory
2. Automatically generating tool-specific formats
3. Using symlinks by default (falling back to copies when needed)
4. Providing both Python and shell interfaces

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## ✨ Features

- Unified `.ai/` folder for all your project-wide AI rules (Markdown)
- Auto-generate:
  - `.cursor/rules/*.mdc`
  - `.cline-rules`
  - `.github/copilot-instructions.md`
  - `devin-guidelines.md`
- Symlink or copy mode (auto-detects OS capability)
- Optional YAML config: `.ai-rules.yml`
- Works with CI and pre-commit hooks

---

## ⚡ Quickstart

```bash
pip install airulefy

# Generate rules for all supported tools
airulefy generate

# Watch for changes in .ai/ and auto-regenerate
airulefy watch
