#!/bin/bash
# install-peon-ping.sh — Install peon-ping (model pack rotation)
# https://github.com/PeonPing/peon-ping
# Pinned to v1.0.0 — update version when upgrading
set -e

PEON_DIR="$HOME/.claude/hooks/peon-ping"

# WSL2 setup
if grep -qi microsoft /proc/version 2>/dev/null; then
    # ffmpeg required for non-WAV sound packs
    if ! command -v ffmpeg >/dev/null 2>&1; then
        echo "==> WSL2 detected — ffmpeg is required for sound pack support."
        echo "   Run the following command manually, then re-run this installer:"
        echo ""
        echo "  sudo apt-get update && sudo apt-get install -y ffmpeg"
        echo ""
        exit 1
    fi

    # Force linux platform so peon-ping uses paplay (WSLg) instead of powershell.exe
    if ! grep -q 'export PLATFORM=linux' "$HOME/.bashrc" 2>/dev/null; then
        echo "==> WSL2 detected — adding PLATFORM=linux to ~/.bashrc for WSLg audio"
        echo 'export PLATFORM=linux' >> "$HOME/.bashrc"
    fi
    export PLATFORM=linux
fi

if [ -f "$PEON_DIR/peon.sh" ]; then
    echo "✓ peon-ping already installed ($PEON_DIR/peon.sh)"
else
    # Sound test at end of installer may fail on WSL2/headless — don't fail the install for it
    # Download to temp file first to avoid curl-pipe-to-shell execution of unverified content
    INSTALL_SCRIPT=$(mktemp)
    curl -fsSL "https://raw.githubusercontent.com/PeonPing/peon-ping/v1.0.0/install.sh" -o "$INSTALL_SCRIPT"
    bash "$INSTALL_SCRIPT" || true
    rm -f "$INSTALL_SCRIPT"
    if [ -f "$PEON_DIR/peon.sh" ]; then
        echo "✓ peon-ping installed"
    else
        echo "✗ peon-ping installation failed"
        exit 1
    fi
fi
