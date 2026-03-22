#!/bin/bash
# uninstall-yq.sh — Remove yq
set -e

if command -v yq >/dev/null 2>&1; then
    echo "To uninstall yq, run the following command manually:"
    echo ""
    echo "  sudo rm -f /usr/local/bin/yq"
    echo ""
    exit 1
else
    echo "✓ yq is not installed"
fi
