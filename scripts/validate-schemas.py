#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["jsonschema>=4.0", "pyyaml>=6.0"]
#
# ///
"""Validate all YAML files and agent frontmatter against JSON schemas."""

import json
import sys
from pathlib import Path

import yaml
from jsonschema import FormatChecker, ValidationError, validate

ROOT = Path(__file__).resolve().parent.parent

# YAML files validated directly
YAML_PAIRS: list[tuple[str, list[str]]] = [
    ("schemas/profiles.schema.json", ["profiles.yaml"]),
    ("schemas/mcps.schema.json", ["src/mcps.yaml"]),
    ("schemas/hooks-meta.schema.json", ["src/hooks-meta.yaml"]),
    ("schemas/statusline.schema.json", ["platforms/claude/statusline.yaml"]),
    (
        "schemas/frontmatter-map.schema.json",
        ["platforms/opencode/frontmatter-map.yaml"],
    ),
]


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from a .md file."""
    if not text.startswith("---"):
        return {}
    try:
        end = text.index("\n---", 3)
    except ValueError:
        print(f"  warning: could not parse frontmatter (no closing ---)")
        return {}
    return yaml.safe_load(text[3:end]) or {}


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


def main() -> None:
    ok = True

    # Validate YAML files
    for schema_path, yaml_paths in YAML_PAIRS:
        schema = json.loads((ROOT / schema_path).read_text())
        for yp in yaml_paths:
            data = yaml.safe_load((ROOT / yp).read_text())
            try:
                validate(instance=data, schema=schema, format_checker=FormatChecker())
                print(f"  ✓ {yp}")
            except ValidationError as e:
                print(f"  ✗ {yp}: {e.message}")
                ok = False

    # Validate agent .md frontmatter
    agent_schema = json.loads((ROOT / "schemas/agent.schema.json").read_text())
    for f in sorted((ROOT / "src" / "agents").rglob("*.md")):
        fm = parse_frontmatter(f.read_text())
        rel = str(f.relative_to(ROOT))
        try:
            validate(instance=fm, schema=agent_schema, format_checker=FormatChecker())
            print(f"  ✓ {rel}")
        except ValidationError as e:
            print(f"  ✗ {rel}: {e.message}")
            ok = False

    # Cross-validate: agent and rule names in profiles must resolve to actual files
    agents_src = ROOT / "src" / "agents"
    rules_src = ROOT / "src" / "rules"
    profiles_data = yaml.safe_load((ROOT / "profiles.yaml").read_text()) or {}
    for profile_name, profile in profiles_data.items():
        if profile_name == "global_rules":
            # global_rules IS the rules section directly (not wrapped in a "rules" key)
            for rule_name in flatten_section(profile):
                if not list(rules_src.rglob(f"{rule_name}.md")):
                    print(f"  ✗ profiles.yaml [global_rules]: rule '{rule_name}' not found in src/rules/")
                    ok = False
            continue
        for agent_name in flatten_section(profile.get("agents") or {}):
            if not list(agents_src.rglob(f"{agent_name}.md")):
                print(
                    f"  ✗ profiles.yaml [{profile_name}]: agent '{agent_name}' not found in src/agents/"
                )
                ok = False
        for rule_name in flatten_section(profile.get("rules") or {}):
            if not list(rules_src.rglob(f"{rule_name}.md")):
                print(
                    f"  ✗ profiles.yaml [{profile_name}]: rule '{rule_name}' not found in src/rules/"
                )
                ok = False

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
