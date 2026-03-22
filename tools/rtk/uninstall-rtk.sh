#!/bin/bash
# uninstall-rtk.sh — Remove rtk (Rust Token Killer)
# https://github.com/rtk-ai/rtk
set -e

if command -v rtk >/dev/null 2>&1; then
    rm -f "$(command -v rtk)"
    echo "✓ rtk binary removed"
else
    echo "✓ rtk is not installed"
fi

# Clean up config
if [ -d "$HOME/.config/rtk" ]; then
    rm -rf "$HOME/.config/rtk"
    echo "✓ rtk config removed"
fi
