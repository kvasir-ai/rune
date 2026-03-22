#!/usr/bin/env python3
"""SubagentStop / Stop hook: pipeline stage guidance.

Reads _pipeline-status.json from the project directory (if present) and
suggests the next step. If no pipeline is active, prints generic guidance.
"""

import json
import os
from pathlib import Path


def main():
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", str(Path.cwd())))
    status_file = project_dir / "_pipeline-status.json"

    if not status_file.exists():
        print("[pipeline] No active pipeline.")
        return

    try:
        state = json.loads(status_file.read_text())
    except (json.JSONDecodeError, OSError):
        return

    workflow = state.get("workflow", "unknown")
    stage = state.get("current_stage", "unknown")
    ticket = state.get("ticket", "none")
    next_agent = state.get("next_agent", "")

    print(
        f"[pipeline] Workflow: {workflow} | Stage completed: {stage} | Ticket: {ticket}"
    )

    if next_agent:
        print(
            f'[pipeline] Suggested next step: Use the {next_agent} subagent on "{ticket}".'
        )
    else:
        print(
            f"[pipeline] All stages complete for {ticket}. Review the final output and approve."
        )


if __name__ == "__main__":
    main()
