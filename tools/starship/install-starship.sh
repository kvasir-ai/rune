#!/bin/bash
# install-starship.sh — Install starship (cross-shell prompt)
# https://github.com/starship/starship
set -e

if ! command -v starship >/dev/null 2>&1; then
    echo "Installing starship via cargo..."
    cargo install starship
    echo "✓ starship installed"
else
    version=$(starship --version 2>/dev/null || echo "unknown")
    echo "✓ starship already installed ($version)"
fi

# Add shell init to bashrc if not present
if ! grep -q 'eval "$(starship init bash)"' "$HOME/.bashrc"; then
    echo '' >> "$HOME/.bashrc"
    echo '# Starship prompt' >> "$HOME/.bashrc"
    echo 'eval "$(starship init bash)"' >> "$HOME/.bashrc"
    echo "✓ starship init added to ~/.bashrc"
else
    echo "✓ starship init already in ~/.bashrc"
fi
