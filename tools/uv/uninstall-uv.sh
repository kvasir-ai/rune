#!/bin/bash
# uninstall-uv.sh — Remove uv
set -e

if command -v uv >/dev/null 2>&1; then
    echo "To uninstall uv, run the following command manually:"
    echo ""
    echo "  uv self uninstall"
    echo ""
    exit 1
else
    echo "✓ uv is not installed"
fi
