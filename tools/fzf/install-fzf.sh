#!/bin/bash
# install-fzf.sh — Install fzf (fuzzy finder)
# https://github.com/junegunn/fzf
# Pinned to v0.60.3 — update version when upgrading
set -e

if ! command -v fzf >/dev/null 2>&1; then
    echo "Installing fzf..."
    git clone --branch v0.60.3 --depth 1 https://github.com/junegunn/fzf.git "$HOME/.fzf"
    "$HOME/.fzf/install" --key-bindings --completion --no-update-rc
    echo "✓ fzf installed"
else
    version=$(fzf --version 2>/dev/null || echo "unknown")
    echo "✓ fzf already installed ($version)"
fi
