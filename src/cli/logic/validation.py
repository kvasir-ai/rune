from __future__ import annotations

import json
from pathlib import Path
import re

from jsonschema import FormatChecker, ValidationError, validate
from ruamel.yaml import YAML

from .._common import flatten_section, parse_frontmatter

_yaml = YAML()
_yaml.preserve_quotes = True

YAML_PAIRS = [
    ('schemas/profiles.schema.json', ['profiles.yaml']),
    ('schemas/mcps.schema.json', ['src/rune-agency/mcps.yaml']),
    ('schemas/hooks-meta.schema.json', ['src/rune-agency/hooks-meta.yaml']),
    ('schemas/statusline.schema.json', ['platforms/claude/statusline.yaml']),
]
OPTIONAL_FILES = {'.local-profile.yaml'}
HOOK_CATEGORIES = {'core', 'explore', 'plan', 'build', 'validate'}
HOOK_COMPANIONS = {
    'core/safety-check': ['core/safety-patterns.yaml'],
    'build/auto-lint': ['build/auto-lint-rules.yaml'],
}


def _strip_fenced_code_blocks(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith('```'):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return '\n'.join(lines)


def validate_schemas(root_dir: Path) -> bool:
    """Validate all project YAML files and agent markdown frontmatter against JSON schemas."""
    ok = True
    for schema_path, yaml_paths in YAML_PAIRS:
        schema_file = root_dir / schema_path
        if not schema_file.exists():
            print(f'  ✗ {schema_path}: schema file not found')
            ok = False
            continue
        schema = json.loads(schema_file.read_text())
        for yp in yaml_paths:
            yp_path = root_dir / yp
            if not yp_path.exists():
                if yp not in OPTIONAL_FILES:
                    print(f'  ✗ {yp}: file not found')
                    ok = False
                continue
            try:
                validate(instance=_yaml.load(yp_path.read_text()), schema=schema, format_checker=FormatChecker())
                print(f'  ✓ {yp}')
            except ValidationError as e:
                print(f'  ✗ {yp}: {e.message}')
                ok = False

    agent_schema_file = root_dir / 'schemas/agent.schema.json'
    if agent_schema_file.exists():
        agent_schema = json.loads(agent_schema_file.read_text())
        for f in sorted((root_dir / 'src' / 'rune-agency' / 'agents').rglob('*.md')):
            fm, _ = parse_frontmatter(f.read_text())
            try:
                validate(instance=fm, schema=agent_schema, format_checker=FormatChecker())
                print(f'  ✓ {f.relative_to(root_dir)}')
            except ValidationError as e:
                print(f'  ✗ {f.relative_to(root_dir)}: {e.message[:120]}')
                ok = False

    skill_phase_pat = re.compile(r'(?m)^phase:\s*(explore|plan|build|validate|general)\s*$')
    for f in sorted((root_dir / 'src' / 'rune-agency' / 'skills').rglob('SKILL.md')):
        text = f.read_text()
        if not text.startswith('---\n'):
            print(f'  ✗ {f.relative_to(root_dir)}: malformed frontmatter opener')
            ok = False
            continue
        if '\n---\n' not in text:
            print(f'  ✗ {f.relative_to(root_dir)}: malformed frontmatter closer')
            ok = False
            continue
        fm, body = parse_frontmatter(text)
        if not fm:
            print(f'  ✗ {f.relative_to(root_dir)}: missing or invalid frontmatter')
            ok = False
            continue
        if not fm.get('description'):
            print(f'  ✗ {f.relative_to(root_dir)}: missing description')
            ok = False
        phase = str(fm.get('phase', ''))
        if phase and phase not in {'explore', 'plan', 'build', 'validate', 'general'}:
            print(f'  ✗ {f.relative_to(root_dir)}: invalid phase "{fm["phase"]}"')
            ok = False
        rel = f.relative_to(root_dir / 'src' / 'rune-agency' / 'skills')
        category = rel.parts[0] if len(rel.parts) > 1 else 'core'
        expected_phase = 'general' if category == 'core' else category
        if phase and phase != expected_phase:
            print(f'  ✗ {f.relative_to(root_dir)}: phase "{phase}" does not match category "{category}"')
            ok = False
        body_no_fences = _strip_fenced_code_blocks(body)
        if skill_phase_pat.search(body_no_fences):
            print(f'  ✗ {f.relative_to(root_dir)}: leaked phase marker in body')
            ok = False
        if category != 'core' and 'src/rune-agency/skills/core/skill-contract/SKILL.md' not in body_no_fences:
            print(f'  ✗ {f.relative_to(root_dir)}: missing shared skill contract reference')
            ok = False

    agency = root_dir / 'src' / 'rune-agency'
    hooks_meta = _yaml.load((agency / 'hooks-meta.yaml').read_text()) if (agency / 'hooks-meta.yaml').exists() else {}
    mcps_data = _yaml.load((agency / 'mcps.yaml').read_text()) if (agency / 'mcps.yaml').exists() else {}
    profiles_data = _yaml.load((root_dir / 'profiles.yaml').read_text()) if (root_dir / 'profiles.yaml').exists() else {}

    FOUNDATION_AGENTS = [
        "explore/knowledge-manager",
        "plan/technical-writer",
        "validate/judge",
        "plan/planner",
        "build/engineer",
    ]
    name_pat = re.compile(r"^[a-z][a-z0-9-]*/[a-z][a-z0-9-]*$")

    def fail(msg: str):
        nonlocal ok
        print(f"  ✗ {msg}")
        ok = False

    hook_dir = agency / 'hooks'
    discovered_hooks: set[str] = set()
    if hook_dir.exists():
        for hook_script in sorted(hook_dir.rglob('*.py')):
            rel = hook_script.relative_to(hook_dir)
            if len(rel.parts) != 2:
                fail(f'hook "{rel}" must live at src/rune-agency/hooks/<phase>/<name>.py')
                continue
            category = rel.parts[0]
            if category not in HOOK_CATEGORIES:
                fail(f'hook "{rel}" uses unknown category "{category}"')
                continue
            hook_name = f'{category}/{hook_script.stem}'
            discovered_hooks.add(hook_name)
            if hook_name not in hooks_meta:
                fail(f'hooks-meta.yaml missing entry for hook "{hook_name}"')

    for hook_name in hooks_meta:
        if not name_pat.match(hook_name):
            fail(f'hooks-meta.yaml: hook "{hook_name}" format invalid')
            continue
        if not (hook_dir / f'{hook_name}.py').exists():
            fail(f'hooks-meta.yaml: hook "{hook_name}" missing script')

    for hook_name, companions in HOOK_COMPANIONS.items():
        if hook_name not in hooks_meta and hook_name not in discovered_hooks:
            continue
        for companion in companions:
            if not (hook_dir / companion).exists():
                fail(f'hook "{hook_name}" missing companion file "{companion}"')

    for pname, prof in profiles_data.items():
        tag = f"profiles.yaml [{pname}]"
        if pname == "global_rules":
            for rname in flatten_section(prof):
                if not name_pat.match(rname):
                    fail(f'{tag}: rule "{rname}" format invalid')
                if not (agency / "rules" / f"{rname}.md").exists():
                    fail(f'{tag}: rule "{rname}" not found')
            continue

        agents = flatten_section(prof.get("agents") or {})
        for aname in agents:
            if not name_pat.match(aname):
                fail(f'{tag}: agent "{aname}" format invalid')
            if not (agency / "agents" / f"{aname}.md").exists():
                fail(f'{tag}: agent "{aname}" not found')
        if any(a in agents for a in FOUNDATION_AGENTS) and not all(
            a in agents for a in FOUNDATION_AGENTS
        ):
            print(
                f'  ℹ {tag}: partial phase agents (missing: {", ".join(a for a in FOUNDATION_AGENTS if a not in agents)})'
            )

        for rname in flatten_section(prof.get("rules") or {}):
            if not name_pat.match(rname):
                fail(f'{tag}: rule "{rname}" format invalid')
            if not (agency / "rules" / f"{rname}.md").exists():
                fail(f'{tag}: rule "{rname}" not found')

        skills = prof.get("skills") or []
        for sname in skills:
            if not name_pat.match(sname):
                fail(f'{tag}: skill "{sname}" format invalid')
            if not (agency / "skills" / sname).is_dir():
                fail(f'{tag}: skill "{sname}" not found')

        for hname in prof.get("hooks") or []:
            if not name_pat.match(hname):
                fail(f'{tag}: hook "{hname}" format invalid')
            if hname not in hooks_meta:
                fail(f'{tag}: hook "{hname}" not in hooks-meta.yaml')
            if not (agency / "hooks" / f"{hname}.py").exists():
                fail(f'{tag}: hook "{hname}" missing script')

        for mname in prof.get('mcps') or []:
            if mname not in mcps_data:
                fail(f'{tag}: mcp "{mname}" not in mcps.yaml')
    return ok
