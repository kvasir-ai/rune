from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from .. import settings
from .models import AvailableContent, RESOURCE_CATEGORIES, Tool
from .profiles import _categorize_md_files
from .._common import yaml_instance

_yaml = yaml_instance()


def discover(_curdir: Path) -> AvailableContent:
    """Discover all available resources in the agency directory."""
    agency = settings.AGENCY_DIR
    content = AvailableContent()
    content.agents = _categorize_md_files(agency / "agents")
    content.rules = _categorize_md_files(agency / "rules")

    skills_dir = agency / "skills"
    if skills_dir.is_dir():
        content.skills = sorted(
            str(skill_file.parent.relative_to(skills_dir))
            for skill_file in skills_dir.rglob("SKILL.md")
        )

    hooks_dir = agency / "hooks"
    if hooks_dir.is_dir():
        found_hooks: list[str] = []
        for category in RESOURCE_CATEGORIES:
            directory = hooks_dir / category
            if directory.is_dir():
                found_hooks.extend(sorted(f"{category}/{path.stem}" for path in directory.glob("*.py")))
        content.hooks = found_hooks

    mcps_file = agency / "mcps.yaml"
    if mcps_file.exists():
        data = _yaml.load(mcps_file.read_text()) or {}
        content.mcps = sorted(data.keys())

    return content


def _tool_is_installed(binary: str, check: str | None) -> bool:
    """Return True when the tool appears to be installed."""
    if check:
        result = subprocess.run(
            ["bash", "-lc", check],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.returncode == 0
    return shutil.which(binary) is not None


def discover_tools(curdir: Path) -> list[Tool]:
    """Discover system tools from the tools registry."""
    registry_file = curdir / "tools" / "registry.yaml"
    if not registry_file.exists():
        return []

    data = _yaml.load(registry_file.read_text()) or {}
    tools: list[Tool] = []
    for name, info in data.items():
        binary = info.get("binary", name)
        description = info.get("description", "")
        check = info.get("check")
        tools.append(
            Tool(
                name=name,
                binary=binary,
                description=description,
                installed=_tool_is_installed(binary, check),
                required="(required)" in description.lower(),
                check=check,
            )
        )
    return tools
