#!/bin/bash
# install-zoxide.sh — Install zoxide (smarter cd)
# https://github.com/ajeetdsouza/zoxide
# Pinned to v0.9.6 — update version when upgrading
set -e

if ! command -v zoxide >/dev/null 2>&1; then
    echo "Installing zoxide..."
    # Download to temp file first to avoid curl-pipe-to-shell execution of unverified content
    INSTALL_SCRIPT=$(mktemp)
    curl -fsSL "https://raw.githubusercontent.com/ajeetdsouza/zoxide/v0.9.6/install.sh" -o "$INSTALL_SCRIPT"
    bash "$INSTALL_SCRIPT"
    rm -f "$INSTALL_SCRIPT"
    echo "✓ zoxide installed"
else
    version=$(zoxide --version 2>/dev/null || echo "unknown")
    echo "✓ zoxide already installed ($version)"
fi

# Add shell init to bashrc if not present
if ! grep -q 'eval "$(zoxide init bash)"' "$HOME/.bashrc"; then
    echo '' >> "$HOME/.bashrc"
    echo '# Zoxide (smarter cd)' >> "$HOME/.bashrc"
    echo 'eval "$(zoxide init bash)"' >> "$HOME/.bashrc"
    echo "✓ zoxide init added to ~/.bashrc"
else
    echo "✓ zoxide init already in ~/.bashrc"
fi
