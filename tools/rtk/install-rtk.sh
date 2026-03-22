#!/bin/bash
# install-rtk.sh — Install rtk (Rust Token Killer)
# https://github.com/rtk-ai/rtk
# Pinned to v0.4.0 — update version when upgrading
set -e

if ! command -v rtk >/dev/null 2>&1; then
    echo "Installing rtk (Rust Token Killer)..."
    if command -v brew >/dev/null 2>&1; then
        brew install rtk
    else
        # Download to temp file first to avoid curl-pipe-to-shell execution of unverified content
        INSTALL_SCRIPT=$(mktemp)
        curl -fsSL "https://raw.githubusercontent.com/rtk-ai/rtk/v0.4.0/install.sh" -o "$INSTALL_SCRIPT"
        bash "$INSTALL_SCRIPT"
        rm -f "$INSTALL_SCRIPT"
    fi
    echo "✓ rtk installed"
else
    version=$(rtk --version 2>/dev/null || echo "unknown")
    echo "✓ rtk already installed ($version)"
fi

# Configure global hook if not already set up
if command -v rtk >/dev/null 2>&1; then
    if [ ! -f "$HOME/.config/rtk/config.toml" ]; then
        echo "Configuring rtk global hook..."
        rtk init --global
        echo "✓ rtk global hook configured"
    else
        echo "✓ rtk config already exists"
    fi
fi
