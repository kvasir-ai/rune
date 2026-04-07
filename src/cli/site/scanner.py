"""Scan rune-agency content (agents, rules, skills) into structured dicts."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Callable

from .._common import parse_frontmatter

_VALID_PHASES = {"explore", "plan", "build", "validate", "general"}


def _parse_frontmatter(text: str) -> dict[str, str]:
    """Extract YAML frontmatter as a flat dict."""
    fm, _ = parse_frontmatter(text)
    return {str(key): str(value) for key, value in fm.items()}


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text()
    except OSError as exc:
        print(f"WARNING: skipping {path}: {exc}", file=sys.stderr)
        return None


def _extract_body(text: str) -> str:
    if not text.startswith("---"):
        return ""
    try:
        end = text.index("\n---", 3)
    except ValueError:
        return ""
    return text[end + 4 :].strip()


def _normalize_phase(phase: str | None, category: str) -> str:
    value = (phase or category).lower()
    return value if value in _VALID_PHASES else "general"


def _scan_grouped(
    base_dir: Path,
    paths: list[Path],
    build_entry: Callable[[Path, str, str], dict],
) -> dict[str, list[dict]]:
    categories: dict[str, list[dict]] = {}
    for path in paths:
        text = _read_text(path)
        if text is None:
            continue
        rel = path.relative_to(base_dir)
        category = rel.parts[0] if len(rel.parts) > 1 else "general"
        categories.setdefault(category, []).append(build_entry(path, text, category))

    for category in categories:
        categories[category].sort(key=lambda item: item["name"])
    return dict(sorted(categories.items()))


def scan_agents(src: Path, root: Path) -> dict[str, list[dict]]:
    """Return agents grouped by category with full frontmatter."""
    agents_dir = src / "agents"
    paths = [path for path in sorted(agents_dir.rglob("*.md")) if path.name != ".gitkeep"]

    def build_entry(path: Path, text: str, category: str) -> dict:
        fm = _parse_frontmatter(text)
        return {
            "name": fm.get("name", path.stem),
            "emoji": fm.get("emoji", ""),
            "description": fm.get("description", ""),
            "model": fm.get("model", ""),
            "color": fm.get("color", ""),
            "tools": fm.get("tools", ""),
            "version": fm.get("version", ""),
            "phase": _normalize_phase(fm.get("phase"), category),
            "rel_path": str(path.relative_to(root)),
            "body": _extract_body(text),
        }

    return _scan_grouped(agents_dir, paths, build_entry)


def _rule_description(text: str, fm: dict[str, str]) -> str:
    if fm.get("description"):
        return fm["description"]

    in_frontmatter = False
    frontmatter_closed = False
    for line in text.splitlines():
        if line.strip() == "---" and not frontmatter_closed:
            in_frontmatter = not in_frontmatter
            if not in_frontmatter:
                frontmatter_closed = True
            continue
        if not in_frontmatter and line.startswith("# "):
            return line.lstrip("# ").strip()
    return ""


def scan_rules(src: Path, root: Path) -> dict[str, list[dict]]:
    """Return rules grouped by category."""
    rules_dir = src / "rules"
    paths = [path for path in sorted(rules_dir.rglob("*.md")) if path.name != "README.md"]

    def build_entry(path: Path, text: str, category: str) -> dict:
        fm = _parse_frontmatter(text)
        phase_match = re.search(
            r"Phase:\s*(explore|plan|build|validate)",
            text,
            re.IGNORECASE,
        )
        return {
            "name": path.stem,
            "description": _rule_description(text, fm),
            "rel_path": str(path.relative_to(root)),
            "phase": _normalize_phase(
                phase_match.group(1) if phase_match else fm.get("phase"),
                category,
            ),
            "emoji": "&#x1F4DA;",
            "model": "",
            "version": "",
            "tools": "",
        }

    return _scan_grouped(rules_dir, paths, build_entry)


def scan_skills(src: Path, root: Path) -> dict[str, list[dict]]:
    """Return skills grouped by category."""
    skills_dir = src / "skills"
    paths = sorted(skills_dir.rglob("SKILL.md"))

    def build_entry(path: Path, text: str, category: str) -> dict:
        fm = _parse_frontmatter(text)
        return {
            "name": fm.get("name", path.parent.name),
            "description": fm.get("description", ""),
            "rel_path": str(path.relative_to(root)),
            "body": _extract_body(text),
            "phase": _normalize_phase(fm.get("phase"), category),
            "emoji": "&#x1F4DD;",
            "model": "",
            "version": "",
            "tools": "",
        }

    return _scan_grouped(skills_dir, paths, build_entry)
