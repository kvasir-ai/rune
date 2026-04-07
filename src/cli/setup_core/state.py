from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .. import settings
from .._common import active_profile_state_file, deploy_short_name, flatten_section, load_managed_state
from .models import CurrentState, Selections
from .profiles import (
    _load_local_profile_yaml,
    _load_profiles_yaml,
    compute_profile_hash,
    load_profile,
)


def compute_content_hash(curdir: Path, selections: Selections) -> str:
    """Compute a stable hash of all source files for a selection."""
    agency = settings.AGENCY_DIR
    entries: list[tuple[str, str]] = []

    for name in flatten_section(selections.agents):
        match = agency / "agents" / f"{name}.md"
        if match.exists():
            entries.append((str(match.relative_to(curdir)), match.read_text()))
    for name in flatten_section(selections.rules):
        match = agency / "rules" / f"{name}.md"
        if match.exists():
            entries.append((str(match.relative_to(curdir)), match.read_text()))
    for name in selections.skills:
        skill_dir = agency / "skills" / name
        if skill_dir.is_dir():
            for path in sorted(skill_dir.rglob("*")):
                if path.is_file():
                    entries.append((str(path.relative_to(curdir)), path.read_text()))
    for name in selections.hooks:
        hook_file = agency / "hooks" / f"{name}.py"
        if hook_file.exists():
            entries.append((str(hook_file.relative_to(curdir)), hook_file.read_text()))
    if selections.hooks:
        meta = agency / "hooks-meta.yaml"
        if meta.exists():
            entries.append((str(meta.relative_to(curdir)), meta.read_text()))
    if selections.mcps:
        mcps_file = agency / "mcps.yaml"
        if mcps_file.exists():
            entries.append((str(mcps_file.relative_to(curdir)), mcps_file.read_text()))

    entries.sort()
    return hashlib.sha256(json.dumps(entries).encode()).hexdigest()[: settings.HASH_LEN]


def check_base_drift(curdir: Path, profile_name: str, stored_hash: str) -> bool:
    """Check if the base profile hash has drifted."""
    try:
        profiles = _load_profiles_yaml(curdir)
    except (FileNotFoundError, ValueError):
        return False
    if profile_name not in profiles:
        return True
    return compute_profile_hash(profiles[profile_name]) != stored_hash


def check_content_drift(curdir: Path, selections: Selections, stored_hash: str) -> bool:
    """Check if the source content hash has drifted."""
    return compute_content_hash(curdir, selections) != stored_hash


def detect_current_state(curdir: Path, claude_dir: Path | None = None) -> CurrentState:
    """Detect the current installation state and check for drift."""
    state_file = active_profile_state_file()
    if state_file is None:
        return CurrentState(status="none")

    name = state_file.read_text().strip()
    try:
        selections = load_profile(curdir, name)
    except (ValueError, FileNotFoundError):
        return CurrentState(status="profile", profile_name=name)

    base_stale = False
    local_data = _load_local_profile_yaml(curdir)
    if name in local_data:
        entry = local_data[name]
        if entry.get("based_on") and entry.get("base_hash"):
            base_stale = check_base_drift(curdir, entry["based_on"], entry["base_hash"])

    content_stale = False
    install_dir = claude_dir or settings.CLAUDE_DIR
    try:
        managed = load_managed_state(install_dir)
        if managed.get("content_hash"):
            content_stale = check_content_drift(curdir, selections, managed["content_hash"])
    except (json.JSONDecodeError, OSError, KeyError):
        pass

    return CurrentState(
        status="profile",
        profile_name=name,
        selections=selections,
        base_stale=base_stale,
        content_stale=content_stale,
    )


def diff_from_base(base: Selections, current: Selections) -> dict:
    """Compute the difference between current selections and a base."""
    result: dict[str, dict[str, list[str]]] = {}
    for section in ("agents", "rules"):
        base_flat = set(flatten_section(getattr(base, section)))
        current_flat = set(flatten_section(getattr(current, section)))
        added = sorted(current_flat - base_flat)
        removed = sorted(base_flat - current_flat)
        if added or removed:
            result[section] = {"added": added, "removed": removed}

    for section in ("skills", "hooks", "mcps"):
        base_set = set(getattr(base, section))
        current_set = set(getattr(current, section))
        added = sorted(current_set - base_set)
        removed = sorted(base_set - current_set)
        if added or removed:
            result[section] = {"added": added, "removed": removed}
    return result


def list_unmanaged(platform_dir: Path, selections: Selections) -> dict[str, list[str]]:
    """List resources in the platform directory not managed by the selection."""
    managed_state = load_managed_state(platform_dir)
    managed_files = {
        section: set(managed_state.get(section, []))
        for section in ("agents", "rules", "hooks", "skills")
    }
    selected = {
        "agents": {f"{deploy_short_name(name)}.md" for name in flatten_section(selections.agents)},
        "rules": {f"{deploy_short_name(name)}.md" for name in flatten_section(selections.rules)},
        "hooks": {f"{deploy_short_name(name)}.py" for name in selections.hooks},
        "skills": {deploy_short_name(name) for name in selections.skills},
    }

    result: dict[str, list[str]] = {}
    for section, ext in (("agents", ".md"), ("rules", ".md"), ("hooks", ".py")):
        directory = platform_dir / section
        if not directory.is_dir():
            continue
        unmanaged = [
            path.name
            for path in sorted(directory.iterdir())
            if path.suffix == ext
            and path.name not in selected[section]
            and path.name not in managed_files[section]
        ]
        if unmanaged:
            result[section] = unmanaged

    skills_dir = platform_dir / "skills"
    if skills_dir.is_dir():
        unmanaged = [
            path.name
            for path in sorted(skills_dir.iterdir())
            if path.is_dir()
            and path.name not in selected["skills"]
            and path.name not in managed_files["skills"]
        ]
        if unmanaged:
            result["skills"] = unmanaged

    return result
