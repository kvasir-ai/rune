"""MCP management commands."""

from __future__ import annotations

from pathlib import Path

import click

from .. import settings
from .._common import (
    ToolkitError,
    load_profiles_yaml,
    ToolkitContext,
    pass_toolkit,
    resolve_profile,
    save_profiles_yaml,
    yaml_instance,
)

_yaml = yaml_instance()


def load_mcps() -> dict:
    """Load mcps.yaml."""
    f = settings.AGENCY_DIR / "mcps.yaml"
    if not f.exists():
        raise ToolkitError(f"mcps.yaml not found at {f}")
    return _yaml.load(f.read_text()) or {}


def enable_item(path: Path, profile: str, section: str, item: str) -> None:
    """Add item to a profile section."""
    data = _yaml.load(path.read_text())

    if profile not in data:
        raise ToolkitError(f"Profile '{profile}' not found")

    items = data[profile].setdefault(section, [])

    if item in items:
        click.echo(f"  \u2013 '{item}' already enabled in profile '{profile}'")
        return

    items.append(item)
    save_profiles_yaml(path, data)
    click.echo(f"\u2713 Enabled '{item}' in profile '{profile}'")


def disable_item(path: Path, profile: str, section: str, item: str) -> None:
    """Remove item from a profile section."""
    data = _yaml.load(path.read_text())

    if profile not in data:
        raise ToolkitError(f"Profile '{profile}' not found")

    items = data[profile].get(section) or []

    if item not in items:
        click.echo(f"  \u2013 '{item}' is not enabled in profile '{profile}'")
        return

    items.remove(item)
    if not items:
        del data[profile][section]

    save_profiles_yaml(path, data)
    click.echo(f"\u2713 Disabled '{item}' from profile '{profile}'")


@click.group("mcp")
def mcp_group() -> None:
    """MCP management commands."""


@mcp_group.command("list")
def mcp_list() -> None:
    """List all available MCPs."""
    click.echo("Available MCPs:")
    for name, defn in load_mcps().items():
        platforms = []
        if "claude" in defn:
            platforms.append("claude")

        desc = defn.get("description", "")
        click.echo(f"  {name:<20} {desc}")
        click.echo(f'  {"":20} platforms: {", ".join(platforms)}')


@mcp_group.command("status")
@click.option("--profile", default=None, help="Profile name (default: active profile)")
@pass_toolkit
def mcp_status(ctx: ToolkitContext, profile: str | None) -> None:
    """Show MCP status for a profile."""
    profile_name = resolve_profile(profile, ctx.curdir)
    profiles = load_profiles_yaml(ctx.curdir)

    if profile_name not in profiles:
        raise ToolkitError(f"Profile '{profile_name}' not found")

    enabled = set(profiles[profile_name].get("mcps") or [])
    click.echo(f"MCP status for profile '{profile_name}':")

    for name, defn in load_mcps().items():
        tag = "[on] " if name in enabled else "[off]"
        desc = defn.get("description", "")
        click.echo(f"  {tag}  {name:<20} {desc}")


@mcp_group.command("enable")
@click.argument("name", metavar="NAME")
@click.option("--profile", default=None, help="Profile name (default: active profile)")
@pass_toolkit
def mcp_enable(ctx: ToolkitContext, name: str, profile: str | None) -> None:
    """Enable an MCP in a profile."""
    mcps = load_mcps()
    if name not in mcps:
        raise ToolkitError(
            f"'{name}' not found in mcps.yaml. Available: {', '.join(mcps.keys())}"
        )

    enable_item(settings.PROFILES_FILE, resolve_profile(profile, ctx.curdir), "mcps", name)


@mcp_group.command("disable")
@click.argument("name", metavar="NAME")
@click.option("--profile", default=None, help="Profile name (default: active profile)")
@pass_toolkit
def mcp_disable(ctx: ToolkitContext, name: str, profile: str | None) -> None:
    """Disable an MCP in a profile."""
    disable_item(settings.PROFILES_FILE, resolve_profile(profile, ctx.curdir), "mcps", name)
