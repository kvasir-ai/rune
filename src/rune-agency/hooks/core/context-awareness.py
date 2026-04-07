#!/usr/bin/env python3
"""Notification hook: warn on high context pressure during active workflows."""

import json
import os
import sys
from pathlib import Path


def load_state() -> dict:
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", str(Path.cwd())))
    state_file = project_dir / ".rune" / "session-state.json"
    if not state_file.exists():
        return {}
    try:
        return json.loads(state_file.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def main() -> None:
    state = load_state()
    if not state:
        return

    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}

    used_pct = int((payload.get("context_window") or {}).get("used_percentage") or 0)
    if used_pct < 80:
        return

    print(
        json.dumps(
            {
                "decision": "continue",
                "additionalContext": (
                    f"[workflow] Context warning: {used_pct}% used. "
                    "Prefer summaries, finish the current task, and avoid loading broad new context."
                ),
            }
        )
    )


if __name__ == "__main__":
    main()
