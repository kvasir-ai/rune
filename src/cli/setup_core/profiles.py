from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .. import settings
from .._common import flatten_section as _flatten_section
from .._common import yaml_instance
from .models import PROFILE_CONTENT_KEYS, RESOURCE_CATEGORIES, Selections

_yaml = yaml_instance()


def variant_name(profile_name: str) -> str:
    """Append ' (custom)' to profile_name if not already present."""
    if profile_name.endswith(" (custom)"):
        return profile_name
    return f"{profile_name} (custom)"


def state_file_for_install_dir(install_dir: Path) -> Path:
    """Return the active-profile state file for the chosen install directory."""
    return (
        Path.cwd() / ".rune" / "current-profile"
        if install_dir != settings.CLAUDE_DIR
        else settings.CURRENT_PROFILE_FILE
    )


def _load_profiles_yaml(_curdir: Path) -> dict:
    """Load profiles.yaml from settings."""
    if not settings.PROFILES_FILE.exists():
        raise FileNotFoundError(f"profiles.yaml not found at {settings.PROFILES_FILE}")
    return _yaml.load(settings.PROFILES_FILE.read_text()) or {}


def _write_yaml(path: Path, data: dict) -> None:
    """Write YAML data to disk using the shared parser configuration."""
    with open(path, "w") as fp:
        _yaml.dump(data, fp)


def compute_profile_hash(profile_dict: dict) -> str:
    """Compute a stable hash of profile content keys."""
    content = {key: profile_dict[key] for key in PROFILE_CONTENT_KEYS if key in profile_dict}
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()[
        : settings.HASH_LEN
    ]


def _load_local_profile_yaml(curdir: Path) -> dict:
    """Load .local-profile.yaml with automatic migration for shared bases."""
    if not settings.LOCAL_PROFILE_FILE.exists():
        return {}
    data = _yaml.load(settings.LOCAL_PROFILE_FILE.read_text()) or {}
    if data and not all(isinstance(v, dict) for v in data.values()):
        return {}

    try:
        profiles = _load_profiles_yaml(curdir)
        shared_names = {k for k in profiles if k != "global_rules"}
    except (FileNotFoundError, ValueError):
        shared_names = set()

    needs_migration = False
    migrated: dict = {}
    for name, entry in data.items():
        if name != "global_rules" and name in shared_names and "based_on" not in entry:
            new_name = variant_name(name)
            new_entry = dict(entry)
            new_entry["based_on"] = name
            new_entry["base_hash"] = compute_profile_hash(profiles[name])
            migrated[new_name] = new_entry
            needs_migration = True
        else:
            migrated[name] = entry

    if needs_migration:
        _write_yaml(settings.LOCAL_PROFILE_FILE, migrated)
        for current_path in (
            Path.cwd() / ".rune" / "current-profile",
            settings.CURRENT_PROFILE_FILE,
        ):
            if current_path.exists():
                current = current_path.read_text().strip()
                if current in data and current not in migrated:
                    current_path.write_text(variant_name(current) + "\n")
    return migrated


def _categorize_md_files(base_dir: Path) -> dict[str, list[str]]:
    """Group markdown files by their category subdirectory."""
    result: dict[str, list[str]] = {}
    if not base_dir.is_dir():
        return result
    for category in RESOURCE_CATEGORIES:
        directory = base_dir / category
        if directory.is_dir():
            names = sorted(f"{category}/{path.stem}" for path in directory.glob("*.md"))
            if names:
                result[category] = names
    return result


def _resolve_name_to_category(name: str, base_dir: Path) -> str:
    """Resolve a resource name to its category."""
    if "/" in name:
        return name.split("/", 1)[0]
    for category in RESOURCE_CATEGORIES:
        if (base_dir / category / f"{name}.md").exists() or (
            base_dir / category / f"{name}.py"
        ).exists():
            return category
    return "general"


def _regroup_by_filesystem(names: list[str], base_dir: Path) -> dict[str, list[str]]:
    """Regroup flat resource names by their filesystem category."""
    result: dict[str, list[str]] = {}
    seen: set[str] = set()
    for name in names:
        if name in seen:
            continue
        seen.add(name)
        category = _resolve_name_to_category(name, base_dir)
        result.setdefault(category, []).append(name)
    return result


def list_profiles(curdir: Path) -> dict[str, str]:
    """List descriptions for all shared and local profiles."""
    profiles = _load_profiles_yaml(curdir)
    shared = {name: entry.get("description", "") for name, entry in profiles.items() if name != "global_rules"}
    local = _load_local_profile_yaml(curdir)
    local_profiles = {
        name: f"[personal] {entry.get('description', '')}".strip()
        for name, entry in local.items()
        if name != "global_rules"
    }
    return {**shared, **local_profiles}


def _build_selections_from_dict(prof: dict, based_on: str, agency: Path) -> Selections:
    """Build a Selections object from a profile dictionary."""
    agents_raw = prof.get("agents")
    agents = (
        _regroup_by_filesystem(_flatten_section(agents_raw), agency / "agents")
        if agents_raw
        else {}
    )
    rules_raw = prof.get("rules")
    rules = (
        _regroup_by_filesystem(_flatten_section(rules_raw), agency / "rules")
        if rules_raw
        else {}
    )
    return Selections(
        based_on=based_on,
        agents=agents,
        rules=rules,
        skills=list(prof.get("skills") or []),
        hooks=list(prof.get("hooks") or []),
        mcps=list(prof.get("mcps") or []),
    )


def load_profile(curdir: Path, name: str) -> Selections:
    """Load a Selections object for a named profile."""
    local = _load_local_profile_yaml(curdir)
    if name in local:
        prof = local[name]
    else:
        profiles = _load_profiles_yaml(curdir)
        if name not in profiles:
            raise ValueError(f"Profile '{name}' not found")
        prof = profiles[name]
    return _build_selections_from_dict(prof, prof.get("based_on") or name, settings.AGENCY_DIR)


def load_base_profile(curdir: Path, name: str) -> Selections:
    """Load a shared base profile Selections object."""
    profiles = _load_profiles_yaml(curdir)
    if name not in profiles:
        raise ValueError(f"Base profile '{name}' not found")
    return _build_selections_from_dict(profiles[name], name, settings.AGENCY_DIR)


def selections_to_profile_dict(selections: Selections) -> dict:
    """Convert a Selections object back to a profile dictionary."""
    profile = {
        "agents": dict(selections.agents),
        "rules": dict(selections.rules),
        "skills": list(selections.skills),
        "hooks": list(selections.hooks),
        "mcps": list(selections.mcps),
    }
    if selections.based_on:
        profile["based_on"] = selections.based_on
    if selections.base_hash:
        profile["base_hash"] = selections.base_hash
    return profile


def export_to_profiles_yaml(curdir: Path, name: str, description: str, selections: Selections) -> None:
    """Export selections to the shared profiles.yaml."""
    profiles = _load_profiles_yaml(curdir)
    entry = selections_to_profile_dict(selections)
    entry["description"] = description
    profiles[name] = entry
    _write_yaml(settings.PROFILES_FILE, profiles)


def export_to_local_profile_yaml(
    curdir: Path, name: str, description: str, selections: Selections
) -> None:
    """Export selections to the personal .local-profile.yaml."""
    local = _load_local_profile_yaml(curdir)
    entry = selections_to_profile_dict(selections)
    entry["description"] = description
    local[name] = entry
    _write_yaml(settings.LOCAL_PROFILE_FILE, local)


def delete_local_profile(curdir: Path, name: str) -> None:
    """Delete a named profile from .local-profile.yaml."""
    local = _load_local_profile_yaml(curdir)
    if name not in local:
        raise ValueError(f"Local profile '{name}' not found")
    del local[name]
    _write_yaml(settings.LOCAL_PROFILE_FILE, local)
