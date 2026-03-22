#!/bin/bash
# install-bat.sh — Install bat (cat with syntax highlighting)
# https://github.com/sharkdp/bat
set -e

if ! command -v bat >/dev/null 2>&1; then
    echo "Installing bat via cargo..."
    cargo install bat
    echo "✓ bat installed"
else
    version=$(bat --version 2>/dev/null || echo "unknown")
    echo "✓ bat already installed ($version)"
fi
