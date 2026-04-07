from __future__ import annotations

import json
import shutil
from pathlib import Path

import click

from ..._common import deploy_short_name, flatten_section
from .files import deploy_hook_companions, inject_agents, sync_dirs, sync_files
from .helpers import load_json_object
from .settings_sync import inject_hooks, inject_mcps


def configure_profile(
    profile: dict,
    platform: str,
    _curdir: Path,
    src: Path,
    claude_dir: Path,
    claude_src: Path,
    managed_set: dict[str, set[str]] | None = None,
) -> None:
    """Deploy profile resources."""
    for subdir in ("agents", "hooks", "rules", "skills"):
        (claude_dir / subdir).mkdir(parents=True, exist_ok=True)

    managed = managed_set or {}

    click.echo("→ Agents")
    if "agents" in profile:
        agent_names = flatten_section(profile["agents"]) if profile["agents"] else []
        platform_agents = claude_src / "agents" if (claude_src / "agents").is_dir() else None
        inject_agents(
            src / "agents",
            claude_dir / "agents",
            agent_names,
            platform,
            platform_agents,
            managed_set=managed.get("agents"),
        )
        if platform_agents:
            for path in platform_agents.glob("*.md"):
                shutil.copy2(path, claude_dir / "agents")
                click.echo(f"  ✓ {path.stem} (platform-specific)")
    else:
        click.echo("  (skipping)")

    click.echo("→ Rules")
    if "rules" in profile:
        rule_names = flatten_section(profile["rules"]) if profile["rules"] else []
        sync_files(
            src / "rules",
            claude_dir / "rules",
            rule_names,
            ".md",
            managed_set=managed.get("rules"),
            name_transform=deploy_short_name,
        )
    else:
        click.echo("  (skipping)")

    click.echo("→ Skills")
    if "skills" in profile:
        sync_dirs(
            src / "skills",
            claude_dir / "skills",
            profile["skills"] or [],
            managed_set=managed.get("skills"),
            name_transform=deploy_short_name,
        )
    else:
        click.echo("  (skipping)")

    click.echo("→ Hooks")
    if "hooks" in profile:
        hook_names = profile["hooks"] or []
        sync_files(
            src / "hooks",
            claude_dir / "hooks",
            hook_names,
            ".py",
            executable=True,
            managed_set=managed.get("hooks"),
            name_transform=lambda name: Path(name).name,
        )
        deploy_hook_companions(src / "hooks", claude_dir / "hooks", hook_names)
    else:
        click.echo("  (skipping)")

    dest_settings = claude_dir / "settings.json"
    if (claude_src / "settings.json").exists():
        base = json.loads((claude_src / "settings.json").read_text())
        existing = load_json_object(dest_settings)
        for key in ("model", "permissions"):
            if key in base:
                existing[key] = base[key]
        dest_settings.write_text(json.dumps(existing, indent=2) + "\n")

    if (src / "hooks-meta.yaml").exists():
        inject_hooks(src / "hooks-meta.yaml", dest_settings, profile.get("hooks") or [])

    if (claude_src / "statusline_command.py").exists():
        dest = claude_dir / "statusline_command.py"
        shutil.copy2(claude_src / "statusline_command.py", dest)
        dest.chmod(dest.stat().st_mode | 0o111)
        if (claude_src / "statusline.yaml").exists():
            shutil.copy2(claude_src / "statusline.yaml", claude_dir / "statusline.yaml")
        if dest_settings.exists():
            cfg = json.loads(dest_settings.read_text())
            cfg["statusLine"] = {"type": "command", "command": f"python3 {dest}"}
            dest_settings.write_text(json.dumps(cfg, indent=2) + "\n")

    click.echo("→ MCPs")
    if profile.get("mcps"):
        inject_mcps(src / "mcps.yaml", dest_settings, profile["mcps"] or [])
    else:
        click.echo("  (skipping)")
