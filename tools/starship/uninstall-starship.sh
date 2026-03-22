#!/bin/bash
# uninstall-starship.sh — Remove starship
set -e

if command -v starship >/dev/null 2>&1; then
    echo "To uninstall starship, run the following commands manually:"
    echo ""
    echo "  cargo uninstall starship"
    echo "  # Remove 'eval \"\$(starship init bash)\"' from ~/.bashrc"
    echo ""
    exit 1
else
    echo "✓ starship is not installed"
fi
