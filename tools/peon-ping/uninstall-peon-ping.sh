#!/bin/bash
# uninstall-peon-ping.sh — Remove peon-ping
# Pinned to v1.0.0 — update version when upgrading
set -e

if test -f "$HOME/.claude/hooks/peon-ping/peon.sh"; then
    # Download to temp file first to avoid curl-pipe-to-shell execution of unverified content
    UNINSTALL_SCRIPT=$(mktemp)
    curl -fsSL "https://raw.githubusercontent.com/PeonPing/peon-ping/v1.0.0/uninstall.sh" -o "$UNINSTALL_SCRIPT"
    bash "$UNINSTALL_SCRIPT"
    rm -f "$UNINSTALL_SCRIPT"
    echo "✓ peon-ping uninstalled"
else
    echo "✓ peon-ping is not installed"
fi
