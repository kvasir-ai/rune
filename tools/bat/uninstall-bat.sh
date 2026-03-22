#!/bin/bash
# uninstall-bat.sh — Remove bat
set -e

if command -v bat >/dev/null 2>&1 || command -v batcat >/dev/null 2>&1; then
    echo "To uninstall bat, run the following command manually:"
    echo ""
    echo "  cargo uninstall bat"
    echo ""
    exit 1
else
    echo "✓ bat is not installed"
fi
