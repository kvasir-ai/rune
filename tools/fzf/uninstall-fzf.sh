#!/bin/bash
# uninstall-fzf.sh — Remove fzf
set -e

if command -v fzf >/dev/null 2>&1; then
    echo "To uninstall fzf, run the following commands manually:"
    echo ""
    echo "  ~/.fzf/uninstall"
    echo "  rm -rf ~/.fzf"
    echo ""
    exit 1
else
    echo "✓ fzf is not installed"
fi
