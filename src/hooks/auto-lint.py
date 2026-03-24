#!/usr/bin/env python3
"""
PostToolUse hook: auto-lint after file writes using configurable rules.

Rules are loaded from auto-lint-rules.yaml (same directory as this script).
Add, remove, or modify rules in that file — no Python changes needed.
"""

import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

RULES_FILE = Path(__file__).parent / "auto-lint-rules.yaml"


def load_rules() -> list[dict]:
    """Load lint rules from YAML file."""
    if not RULES_FILE.is_file():
        return []

    text = RULES_FILE.read_text()

    if yaml is not None:
        return yaml.safe_load(text) or []

    # Minimal YAML parser for list-of-dicts with a commands list.
    rules: list[dict] = []
    current: dict = {}
    in_commands = False
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- extension:"):
            if current:
                rules.append(current)
            current = {"commands": []}
            _, _, val = stripped.partition(":")
            current["extension"] = val.strip().strip("'\"")
            in_commands = False
            continue
        if stripped == "commands:":
            in_commands = True
            continue
        if in_commands and stripped.startswith("- "):
            current.setdefault("commands", []).append(
                stripped[2:].strip().strip("'\"")
            )
            continue
        if ":" in stripped and not stripped.startswith("-"):
            in_commands = False
            key, _, val = stripped.partition(":")
            val = val.strip().strip("'\"")
            current[key.strip()] = val
    if current:
        rules.append(current)
    return rules


def read_json_input() -> dict:
    """Read and parse JSON from stdin."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return {}


def get_file_path(data: dict) -> str:
    """Extract the file path from hook input."""
    return data.get("tool_input", {}).get("file_path", "")


def run_command(cmd_template: str, file_path: str, timeout: int):
    """Run a single lint command, substituting {file} with the file path."""
    cmd_str = cmd_template.replace("{file}", file_path)
    try:
        subprocess.run(
            shlex.split(cmd_str),
            capture_output=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        pass  # Tool not installed — skip silently
    except subprocess.TimeoutExpired:
        print(f"Warning: timed out: {cmd_str}", file=sys.stderr)


def check_condition(condition: str) -> bool:
    """Check if a condition file exists relative to the project root."""
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.cwd()))
    return (project_dir / condition).is_file()


def lint_file(file_path: str):
    """Find matching rules for the file extension and run their commands."""
    if not file_path or not Path(file_path).is_file():
        return

    ext = Path(file_path).suffix.lstrip(".")
    if not ext:
        return

    rules = load_rules()

    for rule in rules:
        if rule.get("extension", "") != ext:
            continue

        condition = rule.get("condition", "")
        if condition and not check_condition(condition):
            continue

        timeout = int(rule.get("timeout", 10))
        commands = rule.get("commands", [])

        for cmd in commands:
            run_command(cmd, file_path, timeout)


def main():
    data = read_json_input()
    file_path = get_file_path(data)
    lint_file(file_path)


if __name__ == "__main__":
    main()
