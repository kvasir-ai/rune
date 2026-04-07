#!/usr/bin/env python3
"""SubagentStop / Stop hook: workflow stage guidance.

Reads `.rune/session-state.json` from the project directory and suggests the
next owner. If no workflow is active, prints generic guidance.
"""

import json
import os
from pathlib import Path


def load_state(project_dir: Path) -> dict | None:
    """Load the current workflow state, if present and valid enough to use."""
    status_file = project_dir / ".rune" / "session-state.json"
    if not status_file.exists():
        return None
    try:
        return json.loads(status_file.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def main():
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", str(Path.cwd())))
    state = load_state(project_dir)
    if state is None:
        print("[workflow] No active workflow.")
        return

    workflow = state.get("workflow", "unknown")
    stage = state.get("current_stage", "unknown")
    wave = state.get("current_wave", 0)
    ticket = state.get("ticket", "none")
    next_agent = state.get("next_agent", "")
    autonomy_mode = state.get("autonomy_mode", "unknown")

    print(
        f"[workflow] Active: {workflow} | stage: {stage} | wave: {wave} | "
        f"ticket: {ticket} | mode: {autonomy_mode}"
    )

    if next_agent:
        print(f'[workflow] Suggested next owner: {next_agent} for "{ticket}".')
    else:
        print(
            f"[workflow] No next owner recorded for {ticket}. Review the current "
            "artifacts, verification evidence, and pause state before advancing."
        )


if __name__ == "__main__":
    main()
