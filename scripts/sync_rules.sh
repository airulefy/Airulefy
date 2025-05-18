#!/bin/bash
# Sync AI rules across tools

set -e

# Check if airulefy is installed
if ! command -v airulefy &> /dev/null; then
    echo "Error: airulefy is not installed. Please install it with: pip install airulefy"
    exit 1
fi

# Parse arguments
FORCE_COPY=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --copy|-c)
            FORCE_COPY=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

# Prepare command
CMD="airulefy generate"

if [ "$FORCE_COPY" = true ]; then
    CMD="$CMD --copy"
fi

if [ "$VERBOSE" = true ]; then
    CMD="$CMD --verbose"
fi

# Run command
echo "Syncing AI rules..."
$CMD

# Validate result
if [ $? -eq 0 ]; then
    echo "AI rules synced successfully."
else
    echo "Error syncing AI rules."
    exit 1
fi
