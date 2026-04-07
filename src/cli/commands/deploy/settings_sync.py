from __future__ import annotations

import json
from pathlib import Path

import click

from ... import settings
from ..._common import deploy_short_name, load_managed_state, save_managed_state, yaml_instance
from .helpers import load_json_object

_yaml = yaml_instance()


def inject_hooks(meta_file: Path, settings_file: Path, names: list[str]) -> None:
    """Wire hooks to platform events."""
    all_meta = _yaml.load(meta_file.read_text()) or {}
    config = load_json_object(settings_file)

    hook_dir = str(settings_file.parent / "hooks")
    managed = set(all_meta.keys())
    existing = config.get("hooks", {})
    cleaned: dict[str, list] = {}

    for event, entries in existing.items():
        kept = [
            entry
            for entry in entries
            if not any(
                f"/{deploy_short_name(name)}.py" in hook.get("command", "")
                for hook in entry.get("hooks", [])
                for name in managed
            )
        ]
        if kept:
            cleaned[event] = kept

    for name in names:
        if name not in all_meta:
            continue
        stem = name.split("/", 1)[1] if "/" in name else name
        hook_def = all_meta[name]
        for event, binding in hook_def.get("events", {}).items():
            entry = {
                "hooks": [
                    {
                        "type": "command",
                        "command": f"{hook_dir}/{stem}.py",
                        "timeout": binding.get("timeout", settings.DEFAULT_TIMEOUT),
                    }
                ]
            }
            if "matcher" in binding:
                entry["matcher"] = binding["matcher"]
            cleaned.setdefault(event, []).insert(0, entry)

    config["hooks"] = cleaned
    settings_file.write_text(json.dumps(config, indent=2) + "\n")


def inject_mcps(mcps_file: Path, dest_file: Path, names: list[str]) -> None:
    """Inject MCP server configs."""
    all_mcps = _yaml.load(mcps_file.read_text()) or {}
    config = load_json_object(dest_file)

    section: dict[str, dict] = {}
    for name in names:
        if name not in all_mcps:
            continue
        cfg = all_mcps[name].get("claude")
        if not cfg:
            continue
        section[name] = cfg
        click.echo(f"  ✓ {name}")

    key = "mcpServers"
    state = load_managed_state(dest_file.parent)
    previously_managed = set(state.get(key, []))
    existing = config.get(key, {})
    external = {name: value for name, value in existing.items() if name not in previously_managed}
    merged = {**external, **section}
    if merged:
        config[key] = merged
    else:
        config.pop(key, None)

    state[key] = list(section.keys())
    save_managed_state(dest_file.parent, state)
    dest_file.write_text(json.dumps(config, indent=2) + "\n")
