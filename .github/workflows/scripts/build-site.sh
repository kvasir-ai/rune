#!/usr/bin/env bash
# Build the documentation site from docs/ into site/
# Called by GitHub Actions workflow and `make site` locally.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SITE_DIR="$REPO_ROOT/site"
DOCS_DIR="$REPO_ROOT/docs"
TEMPLATE="$REPO_ROOT/.github/workflows/scripts/site-index.html"

# Clean
rm -rf "$SITE_DIR"
mkdir -p "$SITE_DIR/docs"

# Assemble
cp "$TEMPLATE" "$SITE_DIR/index.html"
cp "$DOCS_DIR"/*.md "$SITE_DIR/docs/"
cp -r "$DOCS_DIR/assets" "$SITE_DIR/docs/assets" 2>/dev/null || true

echo "Site built: $SITE_DIR"
echo "  index.html + $(ls "$SITE_DIR/docs/"*.md | wc -l) docs"
