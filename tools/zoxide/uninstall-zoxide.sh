#!/bin/bash
# uninstall-zoxide.sh — Remove zoxide
set -e

if command -v zoxide >/dev/null 2>&1; then
    echo "To uninstall zoxide, run the following commands manually:"
    echo ""
    echo "  rm -f ~/.local/bin/zoxide"
    echo "  # Remove 'eval \"\$(zoxide init bash)\"' from ~/.bashrc"
    echo ""
    exit 1
else
    echo "✓ zoxide is not installed"
fi
