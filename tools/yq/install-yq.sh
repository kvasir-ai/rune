#!/bin/bash
# install-yq.sh — Install yq (YAML processor)
# https://github.com/mikefarah/yq
set -e

if ! command -v yq >/dev/null 2>&1; then
    YQ_VERSION=$(curl -s https://api.github.com/repos/mikefarah/yq/releases/latest | grep '"tag_name"' | sed -E 's/.*"([^"]+)".*/\1/')
    echo "✗ yq is not installed. Run the following commands manually:"
    echo ""
    echo "  sudo wget -qO /usr/local/bin/yq \"https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/yq_linux_amd64\""
    echo "  sudo chmod +x /usr/local/bin/yq"
    echo ""
    exit 1
else
    version=$(yq --version 2>/dev/null || echo "unknown")
    echo "✓ yq already installed ($version)"
fi
