"""Metadata commands — skills and tools listing."""

from __future__ import annotations

import click

from .. import settings
from .. import setup_core as core
from .._common import ToolkitContext, parse_frontmatter, pass_toolkit


@click.command("skills")
def resource_skills() -> None:
    """List available skills with descriptions."""
    skills_dir = settings.AGENCY_DIR / "skills"
    if not skills_dir.is_dir():
        return click.echo("No skills found.")

    skill_entries: list[tuple[str, str, str]] = []
    for skill_file in sorted(skills_dir.rglob("SKILL.md")):
        d = skill_file.parent
        rel = d.relative_to(skills_dir)
        category = rel.parts[0] if len(rel.parts) > 1 else (d.name.split("-", 1)[0] if d.name.split("-", 1)[0] in settings.SKILL_CATEGORY_PREFIXES else "")
        fm, _ = parse_frontmatter(skill_file.read_text())
        skill_entries.append((fm.get("name", d.name), fm.get("description", ""), category))

    if not skill_entries:
        return click.echo("No skills found.")

    categorized: dict[str, list[tuple[str, str]]] = {}
    for name, desc, cat in skill_entries:
        categorized.setdefault(cat or "other", []).append((name, desc))

    click.echo("Available skills (invoke with /skill-name):")
    for cat in sorted(categorized):
        if len(categorized) > 1:
            click.echo(f"\n  [{cat}]")
        for name, desc in categorized[cat]:
            if len(desc) > settings.MAX_DESCRIPTION_LEN:
                desc = desc[:settings.MAX_DESCRIPTION_LEN - 1] + "\u2026"
            click.echo(f"  {name:<36s} {desc}")


@click.command("tools")
@pass_toolkit
def resource_tools(ctx: ToolkitContext) -> None:
    """List available system tools with install status."""
    tools = core.discover_tools(ctx.curdir)
    if not tools:
        return click.echo("No tools found.")

    click.echo("Available tools:")
    for tool in tools:
        tag = "[installed]" if tool.installed else "[not installed]"
        click.echo(f"  {tool.name:<14s} {tag:<16s} {tool.description}")
