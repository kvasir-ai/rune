#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
input_file="claude-output.txt"
command_text="${CLAUDE_REPLAY_COMMAND:-claude -p \"<your prompt here>\"}"
final_input_text=""
char_delay="${CLAUDE_REPLAY_CHAR_DELAY:-0.02}"
line_delay="${CLAUDE_REPLAY_LINE_DELAY:-0.10}"
header_enabled=1
input_box_enabled=0
erase_invocation=1

usage() {
  cat <<'EOF'
Usage: replay-output.sh [options] [input_file]

Replay a saved Claude output capture as if it were typed and streamed live.
Intended to be run manually after starting an asciinema recording.

Options:
  --command TEXT       Fake Claude command to type on screen
  --final-input TEXT   Render one more Claude-style input box at the end
  --char-delay SEC     Delay between typed command characters
  --line-delay SEC     Delay between output lines
  --input-box          Render the command in a Claude-style divider box
  --no-header          Disable the Claude Code banner
  --no-clear-prev      Keep the actual script invocation line visible
  -h, --help           Show this help

Environment overrides:
  CLAUDE_REPLAY_COMMAND
  CLAUDE_REPLAY_CHAR_DELAY
  CLAUDE_REPLAY_LINE_DELAY
EOF
}

sleep_for() {
  local duration="$1"
  if [[ "$duration" == "0" || "$duration" == "0.0" || "$duration" == "0.00" ]]; then
    return
  fi
  sleep "$duration"
}

type_text() {
  local text="$1"
  local i char
  for ((i = 0; i < ${#text}; i++)); do
    char="${text:i:1}"
    printf '%s' "$char"
    sleep_for "$char_delay"
  done
}

repeat_char() {
  local char="$1"
  local count="$2"
  local i
  for ((i = 0; i < count; i++)); do
    printf '%s' "$char"
  done
}

print_header() {
  printf ' \033[38;2;232;119;34m▐▛███▜▌\033[0m   \033[1;38;2;245;245;240mClaude Code v2.1.92\033[0m\n'
  printf '\033[38;2;247;147;30m▝▜█████▛▘\033[0m  \033[38;2;224;221;214mSonnet 4.6 · Claude Max\033[0m\n'
  printf '  \033[38;2;176;118;76m▘▘ ▝▝\033[0m    \033[38;2;166;173;186m/kvasir-ai/rune\033[0m\n'
  printf '\n'
}

print_input_box() {
  local text="$1"
  local cols divider_len prefix pad_len
  cols="$(tput cols 2>/dev/null || printf '140')"
  if [[ ! "$cols" =~ ^[0-9]+$ ]] || ((cols < 20)); then
    cols=140
  fi

  divider_len="$cols"
  prefix='❯ '
  pad_len=$((cols - 2 - ${#text}))
  if ((pad_len < 1)); then
    pad_len=1
  fi

  printf '\033[38;2;88;91;98m'
  repeat_char '─' "$divider_len"
  printf '\033[0m\n'

  printf '\033[1;37m%s\033[0m' "$prefix"
  type_text "$text"
  repeat_char ' ' "$pad_len"
  printf '\n'

  printf '\033[38;2;88;91;98m'
  repeat_char '─' "$divider_len"
  printf '\033[0m\n'
}

while (($# > 0)); do
  case "$1" in
    --command)
      if (($# < 2)); then
        printf 'missing value for --command\n' >&2
        usage >&2
        exit 2
      fi
      command_text="$2"
      shift 2
      ;;
    --char-delay)
      char_delay="${2:?missing value for --char-delay}"
      shift 2
      ;;
    --final-input)
      if (($# < 2)); then
        printf 'missing value for --final-input\n' >&2
        usage >&2
        exit 2
      fi
      final_input_text="$2"
      shift 2
      ;;
    --line-delay)
      line_delay="${2:?missing value for --line-delay}"
      shift 2
      ;;
    --input-box)
      input_box_enabled=1
      shift
      ;;
    --no-header)
      header_enabled=0
      shift
      ;;
    --no-clear-prev)
      erase_invocation=0
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      break
      ;;
    -*)
      printf 'Unknown option: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
    *)
      input_file="$1"
      shift
      ;;
  esac
done

if (($# > 0)); then
  printf 'Unexpected arguments: %s\n' "$*" >&2
  usage >&2
  exit 2
fi

if [[ "$input_file" != /* ]]; then
  input_file="$repo_root/$input_file"
fi

if [[ ! -f "$input_file" ]]; then
  printf 'Input file not found: %s\n' "$input_file" >&2
  exit 1
fi

if [[ ! -t 1 ]]; then
  printf 'This replay helper expects an interactive terminal.\n' >&2
  exit 1
fi

# Remove the visible shell command used to launch this helper, then repaint a fake prompt.
if ((erase_invocation)); then
  tput cuu1 2>/dev/null || true
  tput el 2>/dev/null || true
fi

printf '\n'

if ((header_enabled)); then
  print_header
fi

if ((input_box_enabled)); then
  print_input_box "$command_text"
else
  type_text "$command_text"
  printf '\n'
fi
sleep_for "0.35"

while IFS= read -r line || [[ -n "$line" ]]; do
  printf '%s\n' "$line"
  if [[ -z "$line" ]]; then
    sleep_for "0.03"
  else
    sleep_for "$line_delay"
  fi
done < "$input_file"

if [[ -n "$final_input_text" ]]; then
  sleep_for "0.35"
  printf '\n'
  print_input_box "$final_input_text"
fi
