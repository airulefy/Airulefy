# Airulefy

[![Tests](https://github.com/airulefy/Airulefy/actions/workflows/tests.yml/badge.svg)](https://github.com/airulefy/Airulefy/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/airulefy/Airulefy/branch/main/graph/badge.svg)](https://codecov.io/gh/airulefy/Airulefy)
[![PyPI version](https://badge.fury.io/py/airulefy.svg)](https://badge.fury.io/py/airulefy)

**Unify your AI rules. One source of truth, synced across all major AI coding agents.**

Airulefy makes it easy to maintain a single set of rules in `.ai/` and automatically generate or link them to each tool-specific format (Cursor, Copilot, Cline, Devin, etc.).  
No more copy-pasting. No more inconsistent behavior.

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
```

## 🔧 Configuration

Create a `.ai-rules.yml` file in your project root to customize Airulefy's behavior:

```yaml
default_mode: symlink  # or "copy"
tools:
  cursor:
    output: ".cursor/rules/core.mdc"  # custom output path
  cline:
    mode: copy  # override default mode
  copilot: {}  # use defaults
  devin:
    output: "devin-guidelines.md"
```

## 🧩 DevContainer Usage

Airulefy works seamlessly with GitHub Codespaces and VS Code DevContainers:

```bash
# Open in Codespace
gh codespace create -r airulefy/Airulefy

# Or clone and open locally with VS Code
git clone https://github.com/your-username/your-project.git
cd your-project
code .
```

## 🚀 CLI Commands

```bash
# Generate rules (default: symlink if supported)
airulefy generate

# Force copy instead of symlink
airulefy generate --copy

# Watch for changes and auto-regenerate
airulefy watch

# Validate configuration and files
airulefy validate

# List supported tools and their status
airulefy list-tools

# Show version
airulefy --version
```

## 🧠 Philosophy

Airulefy follows the "single source of truth" principle. Keep all your AI coding assistant rules in one place (`.ai/` directory) and let Airulefy handle the synchronization to each tool's specific format.

This ensures:

1. **Consistency** across all AI assistants
2. **Version control** for your AI instructions
3. **Simplicity** in maintaining rules

## 📄 License

MIT © 2025 Kuu
