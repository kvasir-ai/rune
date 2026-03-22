#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["ruamel.yaml>=0.18"]
#
# ///
"""Profile and resource manager for Claude Code and OpenCode."""

import argparse
import json
import os
import shutil
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
# Profile loading
# ──────────────────────────────────────────────────────────────────────────────


def load_profiles(curdir: Path) -> dict:
    """Load profiles.yaml from curdir, die if not found."""
    f = curdir / "profiles.yaml"
    if not f.exists():
        die(f"✗ profiles.yaml not found at {f}")
    return _yaml.load(f.read_text()) or {}


def active_profile(curdir: Path) -> str:
    """Get the currently active profile name, or 'default' if not set."""
    f = curdir / ".current-profile"
    if f.exists():
        return f.read_text().strip()
    return "default"


def get_profile(profiles: dict, name: str) -> dict:
    """Get a profile by name, die if not found."""
    if name == "global_rules":
        die("✗ 'global_rules' is not a profile — it contains rules shared across all profiles")
    if name not in profiles:
        die(f"✗ Profile '{name}' not found")
    return profiles[name]


# ──────────────────────────────────────────────────────────────────────────────
# File and directory synchronization
# ──────────────────────────────────────────────────────────────────────────────


def flatten_section(items: list[str] | dict[str, list[str]]) -> list[str]:
    """Normalize a profile section from either flat list or grouped dict to a flat list of names."""
    if isinstance(items, list):
        return items
    if isinstance(items, dict):
        result = []
        for names in items.values():
            if names:
                result.extend(names)
        return result
    return []


def resolve_all_rules(profiles: dict, profile_name: str) -> list[str]:
    """Merge global_rules + profile-specific rules, deduped, order preserved."""
    global_rules = flatten_section(profiles.get("global_rules", {}))
    profile_rules = flatten_section(profiles.get(profile_name, {}).get("rules", {}))
    return list(dict.fromkeys(global_rules + profile_rules))


def sync_files(
    src: Path, dest: Path, names: list[str], ext: str, executable: bool = False
) -> None:
    """Copy files from src to dest with given extension, reporting status.

    Removes any stale files in dest that are no longer in the profile.
    """
    dest.mkdir(parents=True, exist_ok=True)
    expected = {f"{name}{ext}" for name in names}
    for existing in dest.glob(f"*{ext}"):
        if existing.name not in expected:
            existing.unlink()
            print(f"  – {existing.stem} (removed, no longer in profile)")
    for name in names:
        matches = list(src.rglob(f"{name}{ext}"))
        if len(matches) > 1:
            print(f"  ✗ {name} (ambiguous: found in {len(matches)} locations)")
            continue
        f = matches[0] if matches else src / f"{name}{ext}"
        if f.exists():
            out = dest / f"{name}{ext}"
            shutil.copy2(f, out)
            if executable:
                out.chmod(out.stat().st_mode | 0o111)
            print(f"  ✓ {name}")
        else:
            print(f"  ✗ {name} (not found: {f})")


def sync_dirs(src: Path, dest: Path, names: list[str]) -> None:
    """Copy directories from src to dest, reporting status.

    Removes any stale directories in dest that are no longer in the profile.
    """
    dest.mkdir(parents=True, exist_ok=True)
    for existing in (d for d in dest.iterdir() if d.is_dir()):
        if existing.name not in names:
            shutil.rmtree(existing)
            print(f"  – {existing.name} (removed, no longer in profile)")
    for name in names:
        d = src / name
        if d.is_dir():
            out = dest / name
            shutil.copytree(d, out, dirs_exist_ok=True)
            for f in out.rglob("*.sh"):
                f.chmod(f.stat().st_mode | 0o111)
            print(f"  ✓ {name}")
        else:
            print(f"  ✗ {name} (not found: {d})")


# ──────────────────────────────────────────────────────────────────────────────
# Agent injection — reads .md files, transforms frontmatter for OpenCode
# ──────────────────────────────────────────────────────────────────────────────


def parse_agent_md(text: str) -> tuple[dict, str]:
    """Split an agent .md file into (frontmatter_dict, body_str)."""
    if not text.startswith("---"):
        return {}, text
    try:
        end = text.index("\n---", 3)
    except ValueError:
        preview = text[:50].replace("\n", "\\n")
        print(f"  warning: no closing '---' found in frontmatter (text: '{preview}')", file=sys.stderr)
        return {}, text
    fm = _yaml.load(text[3:end]) or {}
    body = text[end + 4 :].lstrip("\n")
    return dict(fm), body


def transform_frontmatter(fm: dict, fm_map: dict) -> dict:
    """Transform Claude frontmatter to OpenCode format using the mapping."""
    colors = fm_map.get("colors", {})
    models = fm_map.get("models", {})
    tool_kw = fm_map.get("tool_keywords", {})

    out: dict = {}

    # Description: prefer opencode_description if present
    out["description"] = fm.get("opencode_description", fm.get("description", ""))

    # Color: named → hex
    color = fm.get("color", "")
    out["color"] = colors.get(color, color)

    # Model: claude name → opencode ID
    model = fm.get("model", "")
    out["model"] = models.get(model, model)

    # Mode
    mode = fm_map.get("mode")
    if mode:
        out["mode"] = mode

    # Tools: derive booleans from Claude tool string
    tools_str = fm.get("tools", "")
    tools = {k: kw in tools_str for k, kw in tool_kw.items()}
    out["tools"] = tools

    return out


def inject_agents(
    src: Path,
    dest: Path,
    names: list[str],
    platform: str,
    opencode_src: Path | None = None,
    plat_src: Path | None = None,
) -> None:
    """Deploy agent .md files — copy for Claude, transform for OpenCode.

    Removes any stale .md files in dest that are no longer in the profile.
    """
    dest.mkdir(parents=True, exist_ok=True)

    fm_map: dict = {}
    if platform == "opencode" and opencode_src:
        map_file = opencode_src / "frontmatter-map.yaml"
        if map_file.exists():
            fm_map = _yaml.load(map_file.read_text()) or {}

    # Build the expected set of filenames (profile + platform-specific)
    expected: set[str] = {f"{name}.md" for name in names}
    if plat_src and plat_src.is_dir():
        expected |= {f.name for f in plat_src.glob("*.md")}

    # Remove stale agents no longer in the profile
    for existing in dest.glob("*.md"):
        if existing.name not in expected:
            existing.unlink()
            print(f"  – {existing.stem} (removed, no longer in profile)")

    for name in names:
        matches = list(src.rglob(f"{name}.md"))
        if len(matches) > 1:
            print(f"  ✗ {name} (ambiguous: found in {len(matches)} locations)")
            continue
        agent_file = matches[0] if matches else src / f"{name}.md"
        if not agent_file.exists():
            print(f"  ✗ {name} (not found: {agent_file})")
            continue

        if platform == "claude":
            # Copy as-is — .md files already have Claude frontmatter
            shutil.copy2(agent_file, dest / f"{name}.md")
        else:
            # Transform frontmatter for OpenCode
            fm, body = parse_agent_md(agent_file.read_text())
            oc_fm = transform_frontmatter(fm, fm_map)
            with open(dest / f"{name}.md", "w") as out:
                out.write("---\n")
                _yaml.dump(oc_fm, out)
                out.write("---\n\n")
                out.write(body)

        print(f"  ✓ {name}")


# ──────────────────────────────────────────────────────────────────────────────
# Hook wiring injection
# ──────────────────────────────────────────────────────────────────────────────

HOOK_DIRS = {
    "claude": "$HOME/.claude/hooks",
    "opencode": "$HOME/.config/opencode/hooks",
}


def is_managed_hook(entry: dict, managed_names: set[str]) -> bool:
    """Check if hook entry is managed by the profile (to be cleaned)."""
    for h in entry.get("hooks", []):
        cmd = h.get("command", "")
        for name in managed_names:
            if f"/{name}.py" in cmd:
                return True
    return False


def inject_hooks(
    platform: str, meta_file: Path, settings_file: Path, names: list[str]
) -> None:
    """Wire hooks to platform events in settings.json."""
    all_meta = _yaml.load(meta_file.read_text())
    if not all_meta:
        all_meta = {}

    config = {}
    if settings_file.exists():
        content = settings_file.read_text()
        if content:
            config = json.loads(content)

    hook_dir = HOOK_DIRS[platform]

    # Remove stale profile-managed hooks (clean slate before re-adding)
    managed = set(all_meta.keys())
    existing = config.get("hooks", {})
    cleaned: dict[str, list] = {}

    for event, entries in existing.items():
        kept = [e for e in entries if not is_managed_hook(e, managed)]
        if kept:
            cleaned[event] = kept

    # Wire each enabled hook to its events
    for name in names:
        if name not in all_meta:
            continue

        hook_def = all_meta[name]
        for event, binding in hook_def.get("events", {}).items():
            entry: dict = {
                "hooks": [
                    {
                        "type": "command",
                        "command": f"{hook_dir}/{name}.py",
                        "timeout": binding.get("timeout", 30),
                    }
                ]
            }
            if "matcher" in binding:
                entry["matcher"] = binding["matcher"]

            if event not in cleaned:
                cleaned[event] = []
            cleaned[event].insert(0, entry)

    config["hooks"] = cleaned
    settings_file.write_text(json.dumps(config, indent=2) + "\n")


# ──────────────────────────────────────────────────────────────────────────────
# MCP injection
# ──────────────────────────────────────────────────────────────────────────────


def inject_mcps(
    platform: str, mcps_file: Path, dest_file: Path, names: list[str]
) -> None:
    """Inject MCP server configs into destination settings file."""
    all_mcps = _yaml.load(mcps_file.read_text())
    if not all_mcps:
        all_mcps = {}

    config = {}
    if dest_file.exists():
        content = dest_file.read_text()
        if content:
            config = json.loads(content)

    section: dict[str, dict] = {}
    for name in names:
        if name not in all_mcps:
            print(f"  ✗ {name} (not found in {mcps_file})")
            continue

        cfg = all_mcps[name].get(platform)
        if not cfg:
            print(f"  ✗ {name} (no {platform} config in mcps.yaml)")
            continue

        section[name] = cfg
        print(f"  ✓ {name}")

    key = "mcpServers" if platform == "claude" else "mcp"
    # Preserve externally-managed MCP entries (e.g. peon-ping) by tracking which
    # MCPs ai-toolkit has ever managed in a state file next to the settings file.
    # On each run: remove previously-managed MCPs, then add the active profile's MCPs.
    # This ensures stale entries (e.g. old linear/datadog) are cleaned up, while
    # entries written by external tools (e.g. peon-ping) are never touched.
    state_file = dest_file.parent / ".ai-toolkit-managed-mcps.json"
    previously_managed: set[str] = set()
    if state_file.exists():
        try:
            previously_managed = set(json.loads(state_file.read_text()).get(key, []))
        except (json.JSONDecodeError, AttributeError):
            pass

    existing = config.get(key, {})
    # Keep only entries that were never managed by ai-toolkit
    external = {k: v for k, v in existing.items() if k not in previously_managed}
    merged = {**external, **section}
    if merged:
        config[key] = merged
    else:
        config.pop(key, None)

    # Persist the new managed set
    state: dict = {}
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text())
        except (json.JSONDecodeError, AttributeError):
            pass
    state[key] = list(section.keys())
    state_file.write_text(json.dumps(state, indent=2) + "\n")

    dest_file.write_text(json.dumps(config, indent=2) + "\n")


# ──────────────────────────────────────────────────────────────────────────────
# Profile commands
# ──────────────────────────────────────────────────────────────────────────────


def cmd_profile_current(args) -> None:
    """Print the active profile name."""
    print(active_profile(args.curdir))


def cmd_profile_use(args) -> None:
    """Set the active profile."""
    profiles = load_profiles(args.curdir)
    get_profile(profiles, args.profile)  # Validate exists
    (args.curdir / ".current-profile").write_text(args.profile + "\n")
    print(f"✓ Active profile set to: {args.profile}")


def cmd_profile_list(args) -> None:
    """List all available profiles."""
    profiles = load_profiles(args.curdir)
    print("Available profiles:")
    for name in sorted(profiles.keys()):
        if name == "global_rules":
            continue
        print(f"  {name}")


def cmd_profile_show(args) -> None:
    """Show profile contents."""
    profiles = load_profiles(args.curdir)
    profile = get_profile(profiles, args.profile)

    desc = profile.get("description", "(no description)")
    print(f"Profile: {args.profile} — {desc}")

    # Agents — auto-discovered from src/agents/
    src = args.curdir
    all_agents = sorted({f.stem for f in (src / "src" / "agents").rglob("*.md")})
    if all_agents:
        print(f"\n── agents (auto-discovered) ──────────────────────")
        for name in all_agents:
            print(f"    ✓ {name}")

    # Global rules
    global_rules = profiles.get("global_rules")
    if global_rules:
        print(f"\n── rules (global) ────────────────────────────────")
        for category, names in global_rules.items():
            print(f"  [{category}]")
            for name in names or []:
                print(f"    ✓ {name}")

    # Profile-specific rules, hooks, mcps
    for section in ("rules", "hooks", "mcps"):
        items = profile.get(section)
        if not items:
            continue

        label = f"{section} (profile)" if section == "rules" else section
        padding = "─" * (50 - len(label))
        print(f"\n── {label} {padding}")
        if isinstance(items, dict):
            for category, names in items.items():
                print(f"  [{category}]")
                for name in names or []:
                    print(f"    ✓ {name}")
        else:
            for item in items:
                print(f"  [on]  {item}")

    # Skills — auto-discovered from src/skills/
    all_skills = sorted(
        {d.name for d in (src / "src" / "skills").iterdir() if d.is_dir() and (d / "SKILL.md").exists()}
    )
    if all_skills:
        print(f"\n── skills (auto-discovered) ─────────────────────")
        for name in all_skills:
            print(f"    ✓ {name}")

    print()


# ──────────────────────────────────────────────────────────────────────────────
# Configure command
# ──────────────────────────────────────────────────────────────────────────────


def cmd_configure(args) -> None:
    """Sync configuration to agent directories."""
    profiles = load_profiles(args.curdir)
    profile = get_profile(profiles, args.profile)

    is_claude = args.platform == "claude"
    cfg_dir = args.claude_dir if is_claude else args.opencode_dir
    cfg_src = args.claude_src if is_claude else args.opencode_src

    print(f"==> Syncing {cfg_dir} with profile '{args.profile}'")

    for sub in ("agents", "hooks", "rules", "skills"):
        (cfg_dir / sub).mkdir(parents=True, exist_ok=True)

    # Agents — always deploy ALL agents (frontmatter is lightweight)
    print("→ Agents")
    all_agents = sorted(
        {f.stem for f in (args.src / "agents").rglob("*.md")}
    )
    plat_agents = cfg_src / "agents"
    inject_agents(
        args.src / "agents",
        cfg_dir / "agents",
        all_agents,
        args.platform,
        args.opencode_src,
        plat_agents if plat_agents.is_dir() else None,
    )
    if plat_agents.is_dir():
        for f in plat_agents.glob("*.md"):
            shutil.copy2(f, cfg_dir / "agents")
            print(f"  ✓ {f.stem} (platform-specific)")

    # Rules — merge global_rules + profile-specific rules
    print("→ Rules")
    all_rules = resolve_all_rules(profiles, args.profile)
    if all_rules:
        sync_files(args.src / "rules", cfg_dir / "rules", all_rules, ".md")
    else:
        print("  (no rules configured in profile)")

    # Skills — always deploy ALL skills (SKILL.md is lightweight)
    print("→ Skills")
    all_skills = sorted(
        {d.name for d in (args.src / "skills").iterdir() if d.is_dir() and (d / "SKILL.md").exists()}
    )
    sync_dirs(args.src / "skills", cfg_dir / "skills", all_skills)

    # Hooks — deploy .py files and wire event bindings into settings.json
    print("→ Hooks")
    hooks = profile.get("hooks")
    if hooks:
        sync_files(args.src / "hooks", cfg_dir / "hooks", hooks, ".py", executable=True)
    else:
        print("  (no hooks configured in profile)")

    # Platform-specific base settings — merge, don't overwrite.
    # The base template owns "model" and "permissions" only.
    # All other keys (hooks, statusLine, skipDangerousModePermissionPrompt,
    # mcpServers, sandbox, etc.) are preserved from the existing file.
    base_settings = cfg_src / "settings.json"
    if base_settings.exists():
        base = json.loads(base_settings.read_text())
        existing_settings = {}
        dest_settings = cfg_dir / "settings.json"
        if dest_settings.exists():
            content = dest_settings.read_text()
            if content:
                existing_settings = json.loads(content)
        # Merge: base template keys overwrite, existing keys preserved
        for key in ("model", "permissions"):
            if key in base:
                existing_settings[key] = base[key]
        dest_settings.write_text(json.dumps(existing_settings, indent=2) + "\n")

    # Hook wiring — regenerate profile hook bindings in settings.json
    hooks_meta = args.src / "hooks-meta.yaml"
    if hooks and hooks_meta.exists():
        inject_hooks(args.platform, hooks_meta, cfg_dir / "settings.json", hooks)

    # Platform-specific statusline (optional)
    if is_claude:
        sl = cfg_src / "statusline_command.py"
        if sl.exists():
            dest = cfg_dir / "statusline_command.py"
            shutil.copy2(sl, dest)
            dest.chmod(dest.stat().st_mode | 0o111)
            # Deploy statusline config if present
            sl_cfg = cfg_src / "statusline.yaml"
            if sl_cfg.exists():
                shutil.copy2(sl_cfg, cfg_dir / "statusline.yaml")
            # Inject statusLine into settings.json
            settings_path = cfg_dir / "settings.json"
            if settings_path.exists():
                config = json.loads(settings_path.read_text())
                config["statusLine"] = {
                    "type": "command",
                    "command": f"python3 {dest}",
                }
                settings_path.write_text(json.dumps(config, indent=2) + "\n")

    # MCPs
    print("→ MCPs")
    mcps = profile.get("mcps")
    if mcps:
        mcps_file = args.src / "mcps.yaml"
        if is_claude:
            inject_mcps("claude", mcps_file, cfg_dir / "settings.json", mcps)
        else:
            xdg = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
            oc_json = xdg / "opencode" / "opencode.json"
            if oc_json.exists():
                inject_mcps("opencode", mcps_file, oc_json, mcps)
            else:
                print(f"  – opencode.json not found at {oc_json}, skipping")
    else:
        print("  (no MCPs configured in profile)")

    print(f"✓ {args.platform} config synced successfully with profile '{args.profile}'")


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    """Build command-line argument parser."""
    p = argparse.ArgumentParser(prog="resource-manager", description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    # Profile subcommands
    pp = sub.add_parser("profile")
    ps = pp.add_subparsers(dest="subcommand", required=True)

    c = ps.add_parser("current")
    c.add_argument("curdir", nargs="?", type=Path, default=Path.cwd())
    c.set_defaults(func=cmd_profile_current)

    u = ps.add_parser("use")
    u.add_argument("profile")
    u.add_argument("curdir", nargs="?", type=Path, default=Path.cwd())
    u.set_defaults(func=cmd_profile_use)

    ls = ps.add_parser("list")
    ls.add_argument("curdir", nargs="?", type=Path, default=Path.cwd())
    ls.set_defaults(func=cmd_profile_list)

    sh = ps.add_parser("show")
    sh.add_argument("profile")
    sh.add_argument("curdir", nargs="?", type=Path, default=Path.cwd())
    sh.set_defaults(func=cmd_profile_show)

    # Configure subcommand
    cp = sub.add_parser("configure")
    cp.add_argument("--platform", required=True, choices=["claude", "opencode"])
    cp.add_argument("--profile", required=True)
    cp.add_argument("--curdir", required=True, type=Path)
    cp.add_argument("--src", required=True, type=Path)
    cp.add_argument("--claude-dir", required=True, type=Path)
    cp.add_argument("--opencode-dir", required=True, type=Path)
    cp.add_argument("--claude-src", required=True, type=Path)
    cp.add_argument("--opencode-src", required=True, type=Path)
    cp.set_defaults(func=cmd_configure)

    return p


def main() -> None:
    """Parse arguments and run the selected command."""
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
