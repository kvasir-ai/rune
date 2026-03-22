#!/bin/bash
# uninstall-rg.sh — Remove ripgrep
set -e

if command -v rg >/dev/null 2>&1; then
    echo "To uninstall rg, run the following command manually:"
    echo ""
    echo "  sudo apt-get remove -y ripgrep"
    echo ""
    exit 1
else
    echo "✓ rg is not installed"
fi
