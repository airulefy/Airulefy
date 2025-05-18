#!/bin/bash

# Sync AI rules using shell commands
# This script is a fallback for users who prefer shell-based synchronization

set -euo pipefail

# Configuration
PROJECT_ROOT="${1:-$(pwd)}"
AI_DIR="${PROJECT_ROOT}/.ai"
CURSOR_RULES_DIR="${PROJECT_ROOT}/.cursor/rules"
CLINE_RULES_DIR="${PROJECT_ROOT}/.cline-rules"
COPILOT_RULES_DIR="${PROJECT_ROOT}/.github"
DEVIN_RULES_DIR="${PROJECT_ROOT}"

# Create directories if they don't exist
mkdir -p "${CURSOR_RULES_DIR}"
mkdir -p "${CLINE_RULES_DIR}"
mkdir -p "${COPILOT_RULES_DIR}"

# Function to create relative symlink
create_symlink() {
    local source_file="$1"
    local target_file="$2"
    
    # Calculate relative path
    local relative_path
    relative_path=$(realpath --relative-to="$(dirname "${target_file}")" "${source_file}")
    
    # Create symlink
    ln -sf "${relative_path}" "${target_file}"
}

# Process Cursor rules
if [ -d "${AI_DIR}" ]; then
    # Create core.mdc with front matter
    cat > "${CURSOR_RULES_DIR}/core.mdc" << EOF
---
description: AI rules for Cursor
alwaysApply: true
---

EOF
    
    # Add @ references to markdown files
    find "${AI_DIR}" -type f -name "*.md" | while read -r md_file; do
        echo "@.ai/$(realpath --relative-to="${PROJECT_ROOT}" "${md_file}")" >> "${CURSOR_RULES_DIR}/core.mdc"
    done
fi

# Process Cline rules
if [ -d "${AI_DIR}" ]; then
    find "${AI_DIR}" -type f -name "*.md" | while read -r md_file; do
        create_symlink "${md_file}" "${CLINE_RULES_DIR}/$(basename "${md_file}")"
    done
fi

# Process Copilot rules
if [ -d "${AI_DIR}" ]; then
    find "${AI_DIR}" -type f -name "*.md" | while read -r md_file; do
        create_symlink "${md_file}" "${COPILOT_RULES_DIR}/copilot-instructions.md"
    done
fi

# Process Devin rules
if [ -d "${AI_DIR}" ]; then
    find "${AI_DIR}" -type f -name "*.md" | while read -r md_file; do
        create_symlink "${md_file}" "${DEVIN_RULES_DIR}/devin-guidelines.md"
    done
fi

echo "Rules synchronized successfully!" 