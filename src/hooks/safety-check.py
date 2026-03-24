#!/usr/bin/env python3
"""
PreToolUse hook: block dangerous commands using configurable patterns.

Patterns are loaded from safety-patterns.yaml (same directory as this script).
Add, remove, or modify patterns in that file — no Python changes needed.
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

PATTERNS_FILE = Path(__file__).parent / "safety-patterns.yaml"


def load_patterns() -> list[dict]:
    """Load safety patterns from YAML file."""
    if not PATTERNS_FILE.is_file():
        return []

    text = PATTERNS_FILE.read_text()

    if yaml is not None:
        return yaml.safe_load(text) or []

    # Minimal YAML parser for list-of-dicts with string values.
    # Handles the exact format of safety-patterns.yaml without PyYAML.
    patterns: list[dict] = []
    current: dict = {}
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            if current:
                patterns.append(current)
            current = {}
            stripped = stripped[2:].strip()
        if ":" in stripped and not stripped.startswith("-"):
            key, _, val = stripped.partition(":")
            val = val.strip().strip("'\"")
            current[key.strip()] = val
    if current:
        patterns.append(current)
    return patterns


def read_json_input() -> dict:
    """Read and parse JSON from stdin."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return {}


def get_command(data: dict) -> str:
    """Extract the bash command being executed."""
    return data.get("tool_input", {}).get("command", "")


def make_deny_response(reason: str) -> dict:
    """Create a denial response JSON."""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def is_rm_recursive_force(cmd: str) -> bool:
    """Check if a command is 'rm' with both recursive and force flags.

    Catches all variations: rm -rf, rm -fr, rm -rfv, rm -r -f, rm -Rf,
    rm --recursive --force, rm --recursive -f, rm -r --force, and
    any interleaved flags.
    """
    for rm_match in re.finditer(r"(?:^|[;&|]\s*)\brm\b([^;&|]*)", cmd):
        flags = rm_match.group(1)
        has_recursive = bool(
            re.search(r"--recursive\b", flags)
            or re.search(r"-[a-zA-Z]*[rR]", flags)
        )
        has_force = bool(
            re.search(r"--force\b", flags) or re.search(r"-[a-zA-Z]*f", flags)
        )
        if has_recursive and has_force:
            return True
    return False


def resolve_flags(flag_str: str) -> int:
    """Convert flag string ('i') to regex flags."""
    flags = 0
    if flag_str and "i" in flag_str:
        flags |= re.IGNORECASE
    return flags


def check_pattern(pattern: dict, cmd: str) -> str | None:
    """Check a single pattern against a command. Returns message if matched."""
    severity = pattern.get("severity", "block")
    if severity not in ("block", "warn"):
        return None

    # Built-in compound check (rm recursive+force)
    builtin = pattern.get("builtin", "")
    if builtin == "rm_recursive_force":
        if is_rm_recursive_force(cmd):
            return pattern.get("message", "Blocked by safety check")
        return None

    # Regex match
    match_str = pattern.get("match", "")
    if not match_str:
        return None

    flags = resolve_flags(pattern.get("flags", ""))

    if not re.search(match_str, cmd, flags):
        return None

    # Optional second condition (both must match)
    requires = pattern.get("requires", "")
    if requires:
        req_flags = resolve_flags(pattern.get("requires_flags", ""))
        if not re.search(requires, cmd, req_flags):
            return None

    return pattern.get("message", "Blocked by safety check")


def main():
    data = read_json_input()
    cmd = get_command(data)

    if not cmd:
        sys.exit(0)

    patterns = load_patterns()

    for pattern in patterns:
        reason = check_pattern(pattern, cmd)
        if reason:
            print(json.dumps(make_deny_response(reason)))
            return

    sys.exit(0)


if __name__ == "__main__":
    main()
