# Isolated shell init for Rune demo recordings.
# Intentionally avoids the user's normal ~/.bashrc prompt, history, and title hooks.

_rune_demo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export STARSHIP_CONFIG="${STARSHIP_CONFIG:-${_rune_demo_dir}/rune-demo.toml}"
export TERM="${TERM:-xterm-256color}"
export COLORTERM="${COLORTERM:-truecolor}"
export CLICOLOR_FORCE="${CLICOLOR_FORCE:-1}"
export FORCE_COLOR="${FORCE_COLOR:-1}"
export HISTFILE=/dev/null

set +o history
unset PROMPT_COMMAND

eval "$(starship init bash)"
