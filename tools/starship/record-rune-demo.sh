#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cast_file="${1:-rune-demo-recording.cast}"
window_size="${RUNE_DEMO_WINDOW_SIZE:-140x40}"

cd "$repo_root"

export TERM="${TERM:-xterm-256color}"
export COLORTERM="${COLORTERM:-truecolor}"
export CLICOLOR_FORCE="${CLICOLOR_FORCE:-1}"
export FORCE_COLOR="${FORCE_COLOR:-1}"

exec asciinema rec \
  --return \
  --window-size "$window_size" \
  -c "printf 'rune demo\nexit\n' | script -q -e -E never -c 'bash --noprofile --rcfile tools/starship/rune-demo.bashrc -i' /dev/null" \
  --overwrite \
  "$cast_file"
