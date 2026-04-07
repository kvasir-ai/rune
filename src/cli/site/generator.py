"""Site generator orchestrator — assembles all sections into a single HTML file."""
from __future__ import annotations

import shutil
import tomllib
from datetime import datetime, timezone
from pathlib import Path

from .components import agent_grid, skill_table, rules_section
from .javascript import get_javascript
from .render import render_template
from .scanner import scan_agents, scan_rules, scan_skills
from .sections.agency import build_agency
from .sections.core_concept import build_core_concept
from .sections.hooks import build_hooks
from .sections.home import build_home
from .sections.manual_pages import build_manual_pages
from .sections.operating_guides import build_operating_guides
from .sections.reference import build_reference
from .styles import get_styles

GITHUB_BLOB = "https://github.com/kvasir-ai/rune/blob/main"


def generate(root_dir: Path | None = None, site_dir: Path | None = None) -> Path:
    """Generate the documentation site."""
    root = root_dir or Path(__file__).resolve().parent.parent.parent.parent
    src = root / "src" / "rune-agency"
    site = site_dir or (root / "site")
    source_site = root / "site"
    source_assets = source_site / "assets"

    if site.exists():
        preserve_assets = site.resolve() == source_site.resolve()
        for child in site.iterdir():
            if preserve_assets and child.name == "assets":
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    else:
        site.mkdir(parents=True, exist_ok=True)

    agents = scan_agents(src, root)
    rules = scan_rules(src, root)
    skills = scan_skills(src, root)

    total_agents = sum(len(v) for v in agents.values())
    total_rules = sum(len(v) for v in rules.values())
    total_skills = sum(len(v) for v in skills.values())
    build_date = datetime.now(timezone.utc).strftime("%d %b %Y")
    try:
        with open(root / "pyproject.toml", "rb") as f:
            version = tomllib.load(f)["project"]["version"]
    except Exception:
        version = ""

    agents_html = agent_grid(agents, GITHUB_BLOB)
    skills_html = skill_table(skills, GITHUB_BLOB)
    rules_html = rules_section(rules, GITHUB_BLOB)
    num_categories = len(agents)

    home = build_home(total_agents, total_rules, total_skills)
    core = build_core_concept(total_rules)
    operating_guides = build_operating_guides(total_rules)
    agency = build_agency(agents_html, skills_html, total_rules, num_categories, rules_html)
    manual = build_manual_pages(root)
    hooks = build_hooks()
    reference = build_reference(total_rules, total_agents, total_skills)

    html = render_template(
        "base.html",
        version=version,
        build_date=build_date,
        styles=get_styles(),
        js=get_javascript(),
        sections_html=[home, core, operating_guides, agency, manual, hooks, reference],
    )

    idx = site / "index.html"
    idx.write_text(html, encoding="utf-8")

    if source_assets.exists() and site.resolve() != source_site.resolve():
        shutil.copytree(source_assets, site / "assets", dirs_exist_ok=True)

    print(f"Generated {idx} ({idx.stat().st_size:,} bytes)")
    return idx
