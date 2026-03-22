#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["ruamel.yaml>=0.18"]
#
# ///
"""MCP server lifecycle management for profiles.

Note: this script intentionally uses argparse instead of Typer. It is an
internal bootstrap tool called directly by Makefile targets with no user
interaction. Keeping its external dependencies minimal (only ruamel.yaml for
YAML round-tripping) avoids a chicken-and-egg problem where uv/Typer must be
installed before the toolkit itself can be set up.
"""

import argparse
import io
import sys
from pathlib import Path

from ruamel.yaml import YAML

_yaml = YAML()  # round-trip mode: preserves comments and formatting
_yaml.default_flow_style = False
_yaml.allow_unicode = True


# ──────────────────────────────────────────────────────────────────────────────
# Error handling
# ──────────────────────────────────────────────────────────────────────────────


def die(msg: str) -> None:
    print(msg, file=sys.stderr)
    sys.exit(1)


# ──────────────────────────────────────────────────────────────────────────────
# Data loading
# ──────────────────────────────────────────────────────────────────────────────


def load_profiles(curdir: Path) -> dict:
    """Load profiles.yaml from curdir, die if not found."""
    f = curdir / "profiles.yaml"
    if not f.exists():
        die(f"✗ profiles.yaml not found at {f}")
    return _yaml.load(f.read_text()) or {}


def load_mcps(curdir: Path) -> dict:
    """Load mcps.yaml from curdir, die if not found."""
    f = curdir / "src" / "mcps.yaml"
    if not f.exists():
        die(f"✗ mcps.yaml not found at {f}")
    return _yaml.load(f.read_text()) or {}


def active_profile(curdir: Path) -> str:
    """Get the currently active profile name, or 'default' if not set."""
    f = curdir / ".current-profile"
    if f.exists():
        return f.read_text().strip()
    return "default"


def resolve_profile(profile: str | None, curdir: Path) -> str:
    """Resolve profile name: use given profile or active profile."""
    if profile:
        return profile
    return active_profile(curdir)


# ──────────────────────────────────────────────────────────────────────────────
# Profile editing — ruamel.yaml round-trips the file preserving all formatting
# ──────────────────────────────────────────────────────────────────────────────


def save_profiles(path: Path, data: dict) -> None:
    """Write profiles back to disk, preserving formatting and comments."""
    buf = io.StringIO()
    _yaml.dump(data, buf)
    path.write_text(buf.getvalue())


def enable_item(path: Path, profile: str, section: str, item: str) -> None:
    """Add item to a profile section."""
    data = _yaml.load(path.read_text())

    if profile not in data:
        die(f"✗ Profile '{profile}' not found")

    items = data[profile].setdefault(section, [])

    if item in items:
        print(f"  – '{item}' already enabled in profile '{profile}'")
        return

    items.append(item)
    save_profiles(path, data)
    print(f"✓ Enabled '{item}' in profile '{profile}'")


def disable_item(path: Path, profile: str, section: str, item: str) -> None:
    """Remove item from a profile section."""
    data = _yaml.load(path.read_text())

    if profile not in data:
        die(f"✗ Profile '{profile}' not found")

    items = data[profile].get(section) or []

    if item not in items:
        print(f"  – '{item}' is not enabled in profile '{profile}'")
        return

    items.remove(item)
    if not items:
        del data[profile][section]

    save_profiles(path, data)
    print(f"✓ Disabled '{item}' from profile '{profile}'")


# ──────────────────────────────────────────────────────────────────────────────
# CLI commands
# ──────────────────────────────────────────────────────────────────────────────


def cmd_list(args) -> None:
    """List all available MCPs."""
    print("Available MCPs:")
    for name, defn in load_mcps(args.curdir).items():
        platforms = []
        if "claude" in defn:
            platforms.append("claude")
        if "opencode" in defn:
            platforms.append("opencode")

        desc = defn.get("description", "")
        print(f"  {name:<20} {desc}")
        print(f"  {'':20} platforms: {', '.join(platforms)}")


def cmd_status(args) -> None:
    """Show MCP status for a profile."""
    profile_name = resolve_profile(args.profile, args.curdir)
    profiles = load_profiles(args.curdir)

    if profile_name not in profiles:
        die(f"✗ Profile '{profile_name}' not found")

    enabled = set(profiles[profile_name].get("mcps") or [])
    print(f"MCP status for profile '{profile_name}':")

    for name, defn in load_mcps(args.curdir).items():
        tag = "[on] " if name in enabled else "[off]"
        desc = defn.get("description", "")
        print(f"  {tag}  {name:<20} {desc}")


def cmd_enable(args) -> None:
    """Enable an MCP in a profile."""
    mcps = load_mcps(args.curdir)
    if args.name not in mcps:
        print(f"✗ '{args.name}' not found in mcps.yaml")
        print(f"  Available: {', '.join(mcps.keys())}")
        sys.exit(1)

    profiles_file = profiles_path(args.curdir)
    enable_item(
        profiles_file, resolve_profile(args.profile, args.curdir), "mcps", args.name
    )


def cmd_disable(args) -> None:
    """Disable an MCP in a profile."""
    profiles_file = profiles_path(args.curdir)
    disable_item(
        profiles_file, resolve_profile(args.profile, args.curdir), "mcps", args.name
    )


def profiles_path(curdir: Path) -> Path:
    """Return path to profiles.yaml, die if not found."""
    f = curdir / "profiles.yaml"
    if not f.exists():
        die(f"✗ profiles.yaml not found at {f}")
    return f


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    p = argparse.ArgumentParser(prog="mcp-manager", description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    # list command
    sp = sub.add_parser("list")
    sp.add_argument("--curdir", type=Path, default=Path.cwd())
    sp.set_defaults(func=cmd_list)

    # status command
    sp = sub.add_parser("status")
    sp.add_argument("--profile", default=None)
    sp.add_argument("--curdir", type=Path, default=Path.cwd())
    sp.set_defaults(func=cmd_status)

    # enable command
    sp = sub.add_parser("enable")
    sp.add_argument("name")
    sp.add_argument("--profile", default=None)
    sp.add_argument("--curdir", type=Path, default=Path.cwd())
    sp.set_defaults(func=cmd_enable)

    # disable command
    sp = sub.add_parser("disable")
    sp.add_argument("name")
    sp.add_argument("--profile", default=None)
    sp.add_argument("--curdir", type=Path, default=Path.cwd())
    sp.set_defaults(func=cmd_disable)

    return p


def main() -> None:
    """Parse arguments and run the selected command."""
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
