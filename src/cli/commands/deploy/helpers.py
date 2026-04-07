from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path

from ... import settings, setup_core as core
from ...setup_core import Selections
from ..._common import ToolkitError, active_profile_state_file, detect_platforms


def load_json_object(path: Path) -> dict:
    """Load a JSON object from disk, returning an empty dict for missing or empty files."""
    if not path.exists():
        return {}
    content = path.read_text()
    return json.loads(content) if content else {}


def hook_file_name(name: str) -> str:
    """Return the deployed hook filename for a hook resource."""
    from ..._common import deploy_short_name

    return f"{deploy_short_name(name)}.py"


def active_install_dir() -> Path:
    """Resolve the install directory for the currently active profile."""
    state_file = active_profile_state_file()
    if state_file is None or state_file == settings.CURRENT_PROFILE_FILE:
        return settings.CLAUDE_DIR
    return settings.PROJECT_DIR or (Path.cwd() / ".claude")


def silent_apply(
    curdir: Path,
    selections: Selections,
    active_name: str,
    claude_dir: Path | None = None,
) -> None:
    """Apply a profile without emitting command output."""
    platforms = detect_platforms()
    target = claude_dir or settings.CLAUDE_DIR
    with contextlib.redirect_stdout(io.StringIO()):
        core.apply(
            curdir,
            selections,
            platforms=platforms,
            claude_dir=target,
            active_name=active_name,
        )


def export_variant(curdir: Path, selections: Selections, variant: str) -> None:
    """Export a custom profile variant to the local profile file."""
    base_hash: str | None = None
    description = ""
    if selections.based_on:
        try:
            profiles_data = core._load_profiles_yaml(curdir)
            if selections.based_on in profiles_data:
                base_hash = core.compute_profile_hash(profiles_data[selections.based_on])
                description = profiles_data[selections.based_on].get("description", "")
        except (FileNotFoundError, ValueError):
            pass
    selections.base_hash = base_hash
    core.export_to_local_profile_yaml(curdir, variant, description, selections)


def select_install_dir(scope_global: bool, scope_project: bool) -> tuple[Path, str]:
    """Resolve the install target and scope label."""
    if scope_global and scope_project:
        raise ToolkitError("--global and --project are mutually exclusive.")

    if settings.PROJECT_DIR and not scope_global:
        return settings.PROJECT_DIR, "project"
    if scope_project:
        return Path.cwd() / ".claude", "project"

    return settings.CLAUDE_DIR, "global"
