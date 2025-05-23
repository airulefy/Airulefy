# Quickstart

This quickstart guide will help you learn the basics of Airulefy in 5 minutes.

## 1. Prepare Your Project

First, create a directory for your AI rules:

```bash
# In your project's root directory
mkdir -p .ai
```

## 2. Create AI Rule Files

Create Markdown files in the `.ai` directory:

```bash
cat > .ai/main.md << EOL
# Project Rules

Please follow these coding conventions in this project:

## Code Conventions
- Use spaces for indentation (not tabs)
- Use camelCase for variable names
- Use snake_case for function names
- Write comments in English

## Error Handling
- Properly catch exceptions
- Log exceptions
EOL
```

You can create additional rule files as needed:

```bash
cat > .ai/architecture.md << EOL
# Architecture Guidelines

## Layered Architecture
This project follows these layers:
- Presentation layer
- Business logic layer
- Data access layer
EOL
```

## 3. Create a Configuration File (Optional)

Optionally, create a `.ai-rules.yml` configuration file:

```bash
cat > .ai-rules.yml << EOL
default_mode: symlink
tools:
  cursor:
    output: ".cursor/rules/core.mdc"
  cline:
    mode: copy
  copilot: {}
  devin:
    output: "devin-guidelines.md"
EOL
```

## 4. Generate AI Rules

Generate the AI rules for each tool:

```bash
airulefy generate
```

Example output:

```
Successfully generated rule files:
- .cursor/rules/core.mdc [symlink]
- .cline-rules [copy]
- .github/copilot-instructions.md [symlink]
- devin-guidelines.md [symlink]
```

For more detailed output, use the `-v` option:

```bash
airulefy generate -v
```

## 5. Watch Mode (Optional)

You can run a watch mode that automatically regenerates rules when the `.ai` directory changes:

```bash
airulefy watch
```

This will update all tool-specific files whenever you edit a rule file.

## 6. List Supported Tools

To see the list of supported AI tools and their configurations:

```bash
airulefy list-tools
```

## 7. Validate Configuration

To validate the current configuration and rule files:

```bash
airulefy validate
```
