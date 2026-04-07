#!/usr/bin/env python3
"""Notification hook: inject concise workflow discipline for active runs."""

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

    workflow = state.get("workflow", "workflow")
    stage = state.get("current_stage", "unknown")
    ticket = state.get("ticket", "current task")
    context = (
        f"[workflow] Active: {workflow} | stage: {stage} | ticket: {ticket}\n"
        "[workflow] Stay within the active task scope, verify before claiming done, "
        "and hand off to the next agent explicitly."
    )
    print(json.dumps({"decision": "continue", "additionalContext": context}))


if __name__ == "__main__":
    main()
