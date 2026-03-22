#!/bin/bash
# uninstall-fd.sh — Remove fd
set -e

if command -v fd >/dev/null 2>&1 || command -v fdfind >/dev/null 2>&1; then
    echo "To uninstall fd, run the following commands manually:"
    echo ""
    echo "  sudo apt-get remove -y fd-find"
    echo "  sudo rm -f /usr/local/bin/fd"
    echo ""
    exit 1
else
    echo "✓ fd is not installed"
fi
