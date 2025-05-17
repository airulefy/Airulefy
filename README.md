# Airulefy

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
