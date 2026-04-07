"""Common fixtures for rune tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture
def rune_dir(tmp_path: Path) -> Path:
    """Fixture to provide a .rune directory in a temporary path."""
    rd = tmp_path / ".rune"
    rd.mkdir(parents=True, exist_ok=True)
    return rd


@pytest.fixture
def write_state(rune_dir: Path):
    """Fixture to write session-state.json."""

    def _write(state: dict[str, Any] | str):
        state_file = rune_dir / "session-state.json"
        if isinstance(state, str):
            state_file.write_text(state)
        else:
            state_file.write_text(json.dumps(state))

    return _write


@pytest.fixture
def default_state() -> dict[str, Any]:
    """Provide a default session-state dictionary."""
    return {
        "version": "1.0",
        "workflow": "claude-workflow-layer",
        "current_stage": "build",
        "current_wave": 1,
        "ticket": "Test ticket",
        "autonomy_mode": "interactive",
        "next_agent": "judge",
        "tasks": [],
        "updated_at": "2026-04-04T11:30:00Z",
    }
