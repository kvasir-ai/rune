#!/usr/bin/env python3
"""Notification hook: reinforce planning rules during active plan-stage workflows."""

import json
import os
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
    if state.get("current_stage") != "plan":
        return

    context = (
        "[plan] Planning rules:\n"
        "- include explicit verification steps\n"
        "- include completion criteria\n"
        "- align the plan with the current ticket and workflow boundaries\n"
        "- do not claim a phase is complete without fresh evidence"
    )
    print(json.dumps({"decision": "continue", "additionalContext": context}))


if __name__ == "__main__":
    main()
