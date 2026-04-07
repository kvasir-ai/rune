from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import click

from ... import settings, setup_core as core
from ..._common import (
    ToolkitContext,
    ToolkitError,
    _json_out,
    deploy_short_name,
    get_profile,
    load_managed_state,
    pass_toolkit,
    save_managed_state,
)
from .helpers import active_install_dir, export_variant, hook_file_name, select_install_dir, silent_apply
from .profile_sync import configure_profile


@click.command("configure")
@click.option("--profile", required=True, help="Profile name")
@click.option(
    "--global",
    "scope_global",
    is_flag=True,
    default=False,
    help="Install to global assistant directory (default behavior).",
)
@click.option(
    "--project",
    "scope_project",
    is_flag=True,
    default=False,
    help="Install to project-local .claude/ directory in the current repo.",
)
@pass_toolkit
def system_configure(
    ctx: ToolkitContext, profile: str, scope_global: bool, scope_project: bool
) -> None:
    """Sync configuration to agent directories."""
    install_dir, _ = select_install_dir(scope_global, scope_project)

    if not scope_global and not scope_project and install_dir == settings.CLAUDE_DIR:
        click.echo(
            "Warning: installing to global ~/.claude/. "
            "Set RUNE_PROJECT_DIR or use --project to scope to a repo.",
            err=True,
        )

    profiles = core._load_profiles_yaml(ctx.curdir)
    prof = get_profile(profiles, profile)
    merged_rules = core._flatten_section(profiles.get("global_rules", {})) + core._flatten_section(
        prof.get("rules", {})
    )
    prof = dict(prof)
    prof["rules"] = {"merged": merged_rules}

    managed_state = load_managed_state(install_dir)
    managed_set = {
        section: set(managed_state.get(section, []))
        for section in ("agents", "rules", "hooks", "skills")
    }

    click.echo(f"==> Syncing {install_dir} with profile '{profile}'")
    configure_profile(
        prof,
        "claude",
        ctx.curdir,
        settings.AGENCY_DIR,
        install_dir,
        settings.CLAUDE_SRC,
        managed_set,
    )

    agents_flat = core._flatten_section(prof.get("agents") or {})
    deployed_agents = {f"{deploy_short_name(name)}.md" for name in agents_flat}
    if (settings.CLAUDE_SRC / "agents").is_dir():
        deployed_agents |= {path.name for path in (settings.CLAUDE_SRC / "agents").glob("*.md")}

    managed_state.update(
        {
            "agents": sorted(deployed_agents),
            "rules": sorted(f"{deploy_short_name(name)}.md" for name in merged_rules),
            "hooks": sorted(hook_file_name(name) for name in (prof.get("hooks") or [])),
            "skills": sorted(deploy_short_name(name) for name in (prof.get("skills") or [])),
        }
    )
    save_managed_state(install_dir, managed_state)


@click.command("reset")
@click.option(
    "--global",
    "scope_global",
    is_flag=True,
    default=False,
    help="Reset the global assistant directory.",
)
@click.option(
    "--project",
    "scope_project",
    is_flag=True,
    default=False,
    help="Reset the project-local .claude/ directory in the current repo.",
)
def top_reset(scope_global: bool, scope_project: bool) -> None:
    """Remove all managed resources."""
    install_dir, scope_label = select_install_dir(scope_global, scope_project)
    state = load_managed_state(install_dir)
    if not state:
        click.echo("  Nothing to reset.")
        return

    click.echo(f"\n  Claude Code [{scope_label}] ({install_dir}):")
    for section, items in sorted(state.items()):
        if items:
            click.echo(f'    {section}: {", ".join(items)}')

    if click.prompt('\n  Type "delete" to confirm') != "delete":
        click.echo("  Aborted.")
        return

    click.echo(f"\n==> Resetting Claude Code [{scope_label}]")
    for section, ext in settings.EXT_MAP.items():
        for name in state.get(section, []):
            path = install_dir / section / (name if name.endswith(ext) else f"{name}{ext}")
            if path.exists():
                path.unlink()
                click.echo(f"  – {path.relative_to(install_dir)}")

    for dirname in state.get("skills", []):
        path = install_dir / "skills" / dirname
        if path.is_dir():
            shutil.rmtree(path)
            click.echo(f"  – skills/{dirname}/")

    cfg_file = install_dir / "settings.json"
    if cfg_file.exists():
        try:
            config = json.loads(cfg_file.read_text())
            for mcp_key in ("mcpServers", "mcp"):
                managed_mcps = state.get(mcp_key, [])
                section = config.get(mcp_key, {})
                for name in managed_mcps:
                    section.pop(name, None)
                if not section:
                    config.pop(mcp_key, None)
            cfg_file.write_text(json.dumps(config, indent=2) + "\n")
        except (json.JSONDecodeError, KeyError, OSError):
            pass

    state_file = install_dir / settings.MANAGED_STATE_FILE
    if state_file.exists():
        state_file.unlink()
    profile_state_file = (
        Path.cwd() / ".rune" / "current-profile"
        if scope_label == "project"
        else settings.CURRENT_PROFILE_FILE
    )
    if profile_state_file.exists():
        profile_state_file.unlink()
        click.echo(f"  – {profile_state_file.name} removed")
    click.echo("\n  ✓ Reset complete")


@click.command("verify")
@pass_toolkit
def system_verify(ctx: ToolkitContext) -> None:
    """Verify installed resources match managed state."""
    project_profile = Path.cwd() / ".rune" / "current-profile"
    project_dir = settings.PROJECT_DIR or (Path.cwd() / ".claude")
    install_dir = (
        project_dir
        if settings.PROJECT_DIR
        or project_profile.exists()
        or (project_dir / settings.MANAGED_STATE_FILE).exists()
        else settings.CLAUDE_DIR
    )

    state = load_managed_state(install_dir)
    if not state:
        click.echo("==> Not configured.")
        return

    click.echo(f"==> Verifying {install_dir}")
    all_ok = True
    for section, ext in settings.EXT_MAP.items():
        for name in state.get(section, []):
            path = install_dir / section / (name if name.endswith(ext) else f"{name}{ext}")
            if path.exists():
                click.echo(f"  ✓ {section}/{path.name}")
            else:
                click.echo(f"  ✗ {section}/{path.name} (missing)")
                all_ok = False

    for name in state.get("skills", []):
        path = install_dir / "skills" / name
        if path.is_dir():
            click.echo(f"  ✓ skills/{name}/")
        else:
            click.echo(f"  ✗ skills/{name}/ (missing)")
            all_ok = False

    click.echo("==> Verifying tools")
    for tool in core.discover_tools(ctx.curdir):
        if tool.installed:
            click.echo(f"  ✓ {tool.name}")
        else:
            click.echo(f"  – {tool.name} not installed")

    from ..._common import active_profile_state_file

    state_file = active_profile_state_file()
    if state_file is not None:
        scope = "project" if state_file == project_profile else "global"
        click.echo(f"\n  Active profile: {state_file.read_text().strip()} [{scope}]")
    if not all_ok:
        sys.exit(1)
    click.echo("✓ Verified")


@click.command("use")
@click.argument("name", metavar="PROFILE")
@click.option(
    "--global",
    "scope_global",
    is_flag=True,
    default=False,
    help="Install to global assistant directory (default behavior).",
)
@click.option(
    "--project",
    "scope_project",
    is_flag=True,
    default=False,
    help="Install to project-local .claude/ directory in the current repo.",
)
@pass_toolkit
def profile_use(
    ctx: ToolkitContext, name: str, scope_global: bool, scope_project: bool
) -> None:
    """Apply a profile and deploy its resources directly."""
    install_dir, scope_label = select_install_dir(scope_global, scope_project)
    if not scope_global and not scope_project and install_dir == settings.CLAUDE_DIR:
        click.echo(
            "Warning: installing to global ~/.claude/. "
            "Set RUNE_PROJECT_DIR or use --project to scope to a repo.",
            err=True,
        )
    selections = core.load_profile(ctx.curdir, name)
    silent_apply(ctx.curdir, selections, active_name=name, claude_dir=install_dir)
    from ..._common import detect_platforms

    click.echo(f"[{scope_label}] Profile '{name}' activated.")
    _json_out(
        {
            "success": True,
            "profile": name,
            "scope": scope_label,
            "install_dir": str(install_dir),
            "platforms": detect_platforms(),
        }
    )


@click.command("toggle")
@click.option(
    "--type",
    "rtype",
    required=True,
    type=click.Choice(["agent", "rule", "skill", "hook", "mcp"]),
)
@click.argument("name", metavar="NAME")
@pass_toolkit
def profile_toggle(ctx: ToolkitContext, rtype: str, name: str) -> None:
    """Toggle a resource on or off in the current profile."""
    state = core.detect_current_state(ctx.curdir)
    selections = state.selections or core.Selections()
    profile_name = state.profile_name or "custom"
    shared = profile_name in core._load_profiles_yaml(ctx.curdir)
    variant = core.variant_name(profile_name) if shared else profile_name
    selections.based_on = (
        profile_name if not profile_name.endswith(" (custom)") else selections.based_on
    )
    selections.active_name = variant

    attr = rtype if rtype in ("skills", "hooks", "mcps") else f"{rtype}s"
    current = getattr(selections, attr)
    flat = set(core._flatten_section(current)) if rtype in ("agent", "rule") else set(current)
    if name in flat:
        flat.discard(name)
        action = "disabled"
    else:
        flat.add(name)
        action = "enabled"

    if rtype in ("agent", "rule"):
        value = core._regroup_by_filesystem(sorted(flat), settings.AGENCY_DIR / f"{rtype}s")
    else:
        value = sorted(flat)
    setattr(selections, attr, value)

    silent_apply(ctx.curdir, selections, active_name=variant, claude_dir=active_install_dir())
    export_variant(ctx.curdir, selections, variant)
    from ..._common import detect_platforms

    _json_out(
        {
            "success": True,
            "action": action,
            "type": rtype,
            "name": name,
            "platforms": detect_platforms(),
        }
    )


@click.command("reapply")
@pass_toolkit
def profile_reapply(ctx: ToolkitContext) -> None:
    """Re-apply the current active profile."""
    state = core.detect_current_state(ctx.curdir)
    if state.status == "none" or state.selections is None:
        raise ToolkitError("No active profile.")
    install_dir = active_install_dir()
    silent_apply(
        ctx.curdir,
        state.selections,
        active_name=state.profile_name or "",
        claude_dir=install_dir,
    )
    managed = load_managed_state(install_dir)
    from ..._common import detect_platforms

    _json_out(
        {
            "success": True,
            "profile": state.profile_name,
            "platforms": detect_platforms(),
            "content_hash": managed.get("content_hash", ""),
        }
    )


@click.command("delete")
@click.argument("name", metavar="PROFILE")
@pass_toolkit
def profile_delete(ctx: ToolkitContext, name: str) -> None:
    """Delete a local (personal) profile."""
    if name in core._load_profiles_yaml(ctx.curdir):
        raise ToolkitError(f"Cannot delete shared profile '{name}'.")
    core.delete_local_profile(ctx.curdir, name)

    switched_to = None
    project_file = Path.cwd() / ".rune" / "current-profile"
    for profile_file in (project_file, settings.CURRENT_PROFILE_FILE):
        if profile_file.exists() and profile_file.read_text().strip() == name:
            if name.endswith(" (custom)"):
                base = name[: -len(" (custom)")]
                if base in core._load_profiles_yaml(ctx.curdir):
                    silent_apply(
                        ctx.curdir,
                        core.load_profile(ctx.curdir, base),
                        active_name=base,
                        claude_dir=active_install_dir(),
                    )
                    switched_to = base
            else:
                profile_file.unlink(missing_ok=True)

    _json_out({"success": True, "deleted": name, "switched_to": switched_to})
