#!/usr/bin/env python3
"""Stop hook: remind Claude about unresolved workflow tasks."""

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
    if not state:
        return

    tasks = state.get("tasks", [])
    unresolved = [t["id"] for t in tasks if t.get("status") in {"pending", "running", "blocked"}]
    if not unresolved:
        print("[workflow] Completion check: all tracked tasks are resolved. Verify tests and docs before presenting done.")
        return

    unresolved_str = ", ".join(unresolved)
    print(
        "[workflow] Completion check: unresolved tasks remain "
        f"({unresolved_str}). Do not present the workflow as complete without fresh verification."
    )


if __name__ == "__main__":
    main()
