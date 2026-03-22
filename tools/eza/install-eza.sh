#!/bin/bash
# install-eza.sh — Install eza (modern ls replacement)
# https://github.com/eza-community/eza
set -e

if ! command -v eza >/dev/null 2>&1; then
    echo "Installing eza via cargo..."
    cargo install eza
    echo "✓ eza installed"
else
    version=$(eza --version 2>/dev/null | head -1 || echo "unknown")
    echo "✓ eza already installed ($version)"
fi
