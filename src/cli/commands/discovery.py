"""Discovery commands — list resources, current state, profiles, selections."""

from __future__ import annotations

from pathlib import Path

import click

from .. import settings
from .. import setup_core as core
from .._common import (
    yaml_instance,
    parse_frontmatter,
    load_managed_state,
    pass_toolkit,
    ToolkitContext,
    _json_out,
    deploy_short_name,
)

_yaml = yaml_instance()


def _extract_agent_description(path: Path) -> str:
    text = path.read_text()
    fm, _ = parse_frontmatter(text)
    return fm.get("description", "")


def _extract_rule_description(path: Path) -> str:
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("---"):
            continue
        if stripped.startswith(">"):
            stripped = stripped.lstrip("> ").strip()
        if stripped:
            return stripped
    return ""


def _extract_skill_description(skill_dir: Path) -> str:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.exists():
        return ""
    text = skill_file.read_text()
    try:
        fm, body = parse_frontmatter(text)
    except Exception:
        return ""
    if fm.get("description"):
        return fm["description"]
    for line in body.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return stripped
    return ""


def _extract_hook_description(path: Path) -> str:
    text = path.read_text()
    for delim in ('"""', "'''"):
        start = text.find(delim)
        if start == -1:
            continue
        end = text.find(delim, start + 3)
        if end == -1:
            continue
        docstring = text[start + 3 : end].strip()
        first_line = docstring.splitlines()[0].strip() if docstring else ""
        return first_line
    return path.stem


def _get_deployed_resources() -> dict[str, set[str]]:
    result: dict[str, set[str]] = {
        "agents": set(),
        "rules": set(),
        "hooks": set(),
        "skills": set(),
        "mcps": set(),
    }
    if settings.CLAUDE_DIR.exists():
        state = load_managed_state(settings.CLAUDE_DIR)
        result["agents"] |= {Path(n).stem for n in state.get("agents", [])}
        result["rules"] |= {Path(n).stem for n in state.get("rules", [])}
        result["hooks"] |= {Path(n).stem for n in state.get("hooks", [])}
        result["skills"] |= set(state.get("skills", []))
        result["mcps"] |= set(state.get("mcpServers", []))
        result["mcps"] |= set(state.get("mcp", []))
    return result
@click.command("list")
@pass_toolkit
def resource_list(ctx: ToolkitContext) -> None:
    """List available resources with deployment status."""
    content = core.discover(ctx.curdir)
    deployed = _get_deployed_resources()
    res = {s: [] for s in ("agents", "rules", "skills", "hooks", "mcps")}

    for cat, names in content.agents.items():
        for name in names:
            p = settings.AGENCY_DIR / "agents" / f"{name}.md"
            res["agents"].append({"name": name, "category": cat, "deployed": name.split("/")[-1] in deployed["agents"], "description": _extract_agent_description(p) if p.exists() else ""})

    for cat, names in content.rules.items():
        for name in names:
            p = settings.AGENCY_DIR / "rules" / f"{name}.md"
            res["rules"].append({"name": name, "category": cat, "deployed": name.split("/")[-1] in deployed["rules"], "description": _extract_rule_description(p) if p.exists() else ""})

    for name in content.skills:
        d = settings.AGENCY_DIR / "skills" / name
        res["skills"].append({"name": name, "deployed": name.split("/")[-1] in deployed["skills"], "description": _extract_skill_description(d)})

    for name in content.hooks:
        p = settings.AGENCY_DIR / "hooks" / f"{name}.py"
        res["hooks"].append({"name": name, "deployed": deploy_short_name(name) in deployed["hooks"], "description": _extract_hook_description(p) if p.exists() else name})

    mcp_data = _yaml.load((settings.AGENCY_DIR / "mcps.yaml").read_text()) or {} if (settings.AGENCY_DIR / "mcps.yaml").exists() else {}
    for name in content.mcps:
        res["mcps"].append({"name": name, "deployed": name in deployed["mcps"], "description": mcp_data.get(name, {}).get("description", name)})

    _json_out(res)


@click.command("status")
@pass_toolkit
def system_status(ctx: ToolkitContext) -> None:
    """Show current deployment state."""
    state = core.detect_current_state(ctx.curdir)
    sel = state.selections
    global_dir = settings.CLAUDE_DIR
    project_dir = Path.cwd() / ".claude"
    global_state = load_managed_state(global_dir) if global_dir.exists() else {}
    project_state = load_managed_state(project_dir) if project_dir.exists() else {}
    _json_out({
        "profile": state.profile_name,
        "based_on": sel.based_on if sel else None,
        "base_stale": state.base_stale,
        "content_stale": state.content_stale,
        "scope": {
            "global": {
                "dir": str(global_dir),
                "installed": bool(global_state),
                "profile": global_state.get("profile"),
            },
            "project": {
                "dir": str(project_dir),
                "installed": bool(project_state),
                "profile": project_state.get("profile"),
            },
        },
        "agents": dict(sel.agents) if sel else {},
        "rules": dict(sel.rules) if sel else {},
        "skills": list(sel.skills) if sel else [],
        "hooks": list(sel.hooks) if sel else [],
        "mcps": list(sel.mcps) if sel else [],
    })


@click.command("list")
@pass_toolkit
def profile_list(ctx: ToolkitContext) -> None:
    """List all available profiles."""
    if ctx.format == "json":
        res = []
        for name, prof in core._load_profiles_yaml(ctx.curdir).items():
            if name != "global_rules":
                res.append(
                    {
                        "name": name,
                        "description": prof.get("description", ""),
                        "source": "shared",
                    }
                )
        for name, prof in core._load_local_profile_yaml(ctx.curdir).items():
            if name != "global_rules":
                res.append(
                    {
                        "name": name,
                        "description": prof.get("description", ""),
                        "source": "local",
                        "based_on": prof.get("based_on"),
                    }
                )
        _json_out(res)
    else:
        profiles = core._load_profiles_yaml(ctx.curdir)
        click.echo("Available profiles:")
        for name in sorted(profiles.keys()):
            if name != "global_rules":
                click.echo(f"  {name}")


@click.command("show")
@click.argument("name", metavar="PROFILE")
@pass_toolkit
def profile_show(ctx: ToolkitContext, name: str) -> None:
    """Output full resource selections for a profile."""
    sel = core.load_profile(ctx.curdir, name)
    _json_out({
        "agents": core._flatten_section(sel.agents),
        "rules": core._flatten_section(sel.rules),
        "skills": list(sel.skills),
        "hooks": list(sel.hooks),
        "mcps": list(sel.mcps),
    })
