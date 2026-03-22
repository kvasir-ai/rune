#!/bin/bash
# uninstall-eza.sh — Remove eza
set -e

if command -v eza >/dev/null 2>&1; then
    echo "To uninstall eza, run the following command manually:"
    echo ""
    echo "  cargo uninstall eza"
    echo ""
    exit 1
else
    echo "✓ eza is not installed"
fi
