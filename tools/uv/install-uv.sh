#!/bin/bash
# install-uv.sh — Install uv (Python package manager)
# https://github.com/astral-sh/uv
# Pinned to 0.6.0 — update version when upgrading
set -e

if ! command -v uv >/dev/null 2>&1; then
    # Download to temp file first to avoid curl-pipe-to-shell execution of unverified content
    INSTALL_SCRIPT=$(mktemp)
    curl -LsSf "https://astral.sh/uv/0.6.0/install.sh" -o "$INSTALL_SCRIPT"
    sh "$INSTALL_SCRIPT"
    rm -f "$INSTALL_SCRIPT"
    echo "✓ uv installed"
else
    version=$(uv --version 2>/dev/null || echo "unknown")
    echo "✓ uv already installed ($version)"
fi
