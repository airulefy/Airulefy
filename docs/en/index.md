# Airulefy

![PyPI](https://img.shields.io/pypi/v/airulefy)
![License](https://img.shields.io/github/license/airulefy/Airulefy)

**Unify your AI rules. One source of truth, synced across all major AI coding agents.**

Airulefy makes it easy to maintain a single set of rules in `.ai/` directory and automatically generate or link them to each tool-specific format (Cursor, Copilot, Cline, Devin, etc.).
No more copy-pasting. No more inconsistent behavior.

## Key Features

- Unified `.ai/` folder for all your project-wide AI rules (Markdown)
- Auto-generate:
  - `.cursor/rules/*.mdc`
  - `.cline-rules`
  - `.github/copilot-instructions.md`
  - `devin-guidelines.md`
- Symlink or copy mode (auto-detects OS capability)
- Optional YAML config: `.ai-rules.yml`
- Works with CI and pre-commit hooks

## Why Airulefy?

As AI-driven development tools become more prevalent, each tool receives instructions in its own format and location. This makes it difficult to maintain when using multiple tools, as you need to update the same instructions in multiple places.

Airulefy solves this problem by automatically generating or linking files from a single source of truth to the format needed by each AI tool.
