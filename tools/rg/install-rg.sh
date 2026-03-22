#!/bin/bash
# install-rg.sh — Install ripgrep (fast recursive search)
# https://github.com/BurntSushi/ripgrep
set -e

if ! command -v rg >/dev/null 2>&1; then
    echo "✗ rg is not installed. Run the following command manually:"
    echo ""
    echo "  sudo apt-get update && sudo apt-get install -y ripgrep"
    echo ""
    exit 1
else
    version=$(rg --version 2>/dev/null | head -1 || echo "unknown")
    echo "✓ rg already installed ($version)"
fi
