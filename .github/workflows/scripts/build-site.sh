#!/usr/bin/env bash
# Build the documentation site into site/ using the Python generator.
# Kept aligned with the GitHub Pages build and useful locally.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SITE_DIR="$REPO_ROOT/site"

# Clean generated output but preserve tracked source assets.
mkdir -p "$SITE_DIR/assets"
find "$SITE_DIR" -mindepth 1 -maxdepth 1 ! -name assets -exec rm -rf {} +

# Generate the authoritative docs site from src/cli/site/.
PYTHONPATH="$REPO_ROOT/src" uv run python -m cli --source-dir "$REPO_ROOT" system site --output "$SITE_DIR"

echo "Site built: $SITE_DIR"
echo "  index.html + tracked assets preserved in site/assets"
