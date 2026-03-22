#!/bin/bash
# install-fd.sh — Install fd (fast file finder)
# https://github.com/sharkdp/fd
set -e

if ! command -v fd >/dev/null 2>&1 && ! command -v fdfind >/dev/null 2>&1; then
    echo "✗ fd is not installed. Run the following commands manually:"
    echo ""
    echo "  sudo apt-get update && sudo apt-get install -y fd-find"
    echo "  sudo ln -sf \$(which fdfind) /usr/local/bin/fd"
    echo ""
    exit 1
else
    version=$(fd --version 2>/dev/null || fdfind --version 2>/dev/null || echo "unknown")
    echo "✓ fd already installed ($version)"
fi
