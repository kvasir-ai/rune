---
description: "Audit Rune Agency knowledge health: rules, skills, docs canon, cross-references, profile wiring, and context budget. Use after major changes or periodically."
user_invocable: true
phase: explore
---

# Knowledge Base Audit

Shared contract: apply `src/rune-agency/skills/core/skill-contract/SKILL.md`
before following the phase-specific steps below.

You are auditing the Rune Agency knowledge layer for health issues. Run all
checks and produce a consolidated report grounded in the current canon.

## Before You Start

Determine the workspace root and locate the toolkit structure:

```bash
WORKSPACE_ROOT="$(pwd)"

# Find rules directory
RULES_DIR=""
[ -d "src/rune-agency/rules" ] && RULES_DIR="src/rune-agency/rules"

# Find skills directory
SKILLS_DIR=""
[ -d "src/rune-agency/skills" ] && SKILLS_DIR="src/rune-agency/skills"

# Find profiles
PROFILES=""
[ -f "profiles.yaml" ] && PROFILES="profiles.yaml"
```

---

## Check 1: Documentation And Artifact Canon

Verify tracked vs ephemeral artifact placement:

```bash
rg -n "docs/adrs|make use-profile|make validate" src/rune-agency docs README.md AGENTS.md CONTRIBUTING.md site 2>/dev/null
```

Check tracked decision and plan surfaces:
```bash
find docs -maxdepth 3 -type f \( -name "*.md" -o -name "*.yaml" \) 2>/dev/null | sort
```

---

## Check 2: Hook Bundle Integrity

Audit hooks as a bundled runtime surface:

```bash
find src/rune-agency/hooks -maxdepth 3 -type f | sort
sed -n '1,220p' src/rune-agency/hooks-meta.yaml
rg -n "core/safety-check|build/auto-lint|hooks-meta|session-state|hook" AGENTS.md README.md src/rune-agency src/cli tests -g '!site/assets/**'
```

Flag:
- hook script without `hooks-meta.yaml` entry
- `hooks-meta.yaml` entry without script
- missing companion config for hook-driven rules
- stale flat hook paths or uncategorized hook names in docs, rules, or profiles

---

## Check 3: Rule Quality

For each rule in `$RULES_DIR`:

**Size check:**
```bash
find "$RULES_DIR" -name "*.md" -exec wc -l {} + | sort -rn | head -20
```

Flag: >800 lines (bloated, must split), <50 lines (consider merging).

**Staleness check:**
```bash
find "$RULES_DIR" -name "*.md" -mtime +180 -exec ls -la {} \;
```

Flag rules not modified in 6+ months that contain version-specific content.

**Structure check** — each rule should have:
- Header block (`>` quoted lines with description and source)
- Horizontal rules separating sections
- Cross-references section at the bottom

---

## Check 4: Orphan Rules And Skills

Rules or skills that exist but are not referenced by any profile:

```bash
if [ -n "$PROFILES" ]; then
  find "$RULES_DIR" -name "*.md" | sed "s#^$RULES_DIR/##; s#\.md\$##" | sort > /tmp/all_rules.txt
  python - <<'PY' > /tmp/profiled_resources.txt
from pathlib import Path
from ruamel.yaml import YAML
yaml = YAML()
data = yaml.load(Path("profiles.yaml").read_text()) or {}
values = set()
for name, profile in data.items():
    if name == "global_rules":
        for section in (profile or {}).values():
            for item in section or []:
                values.add(item)
        continue
    for section_name in ("rules", "skills"):
        section = (profile or {}).get(section_name) or {}
        if isinstance(section, dict):
            for items in section.values():
                for item in items or []:
                    values.add(item)
        else:
            for item in section or []:
                values.add(item)
print("\n".join(sorted(values)))
PY
  echo "=== Orphaned rules (not in any profile) ==="
  comm -23 /tmp/all_rules.txt /tmp/profiled_resources.txt
  if [ -n "$SKILLS_DIR" ]; then
    find "$SKILLS_DIR" -name "SKILL.md" | sed "s#^$SKILLS_DIR/##; s#/SKILL\.md\$##" | sort > /tmp/all_skills.txt
    echo "=== Orphaned skills (not in any profile) ==="
    comm -23 /tmp/all_skills.txt /tmp/profiled_resources.txt
  fi
fi
```

---

## Check 5: Broken Cross-References And Skill Frontmatter

```bash
if [ -n "$RULES_DIR" ]; then
  grep -rh 'src/rune-agency/rules/.*\.md' "$RULES_DIR" "$SKILLS_DIR" 2>/dev/null | \
    grep -oP 'src/rune-agency/rules/[a-z0-9/-]+\.md' | sort -u | while read ref; do
      if [ ! -f "$ref" ]; then
        echo "BROKEN: $ref"
      fi
    done
fi

if [ -n "$SKILLS_DIR" ]; then
  python - <<'PY'
from pathlib import Path
import re
skills = sorted(Path("src/rune-agency/skills").rglob("SKILL.md"))
for skill in skills:
    text = skill.read_text()
    if not text.startswith("---\n"):
        print(f"MALFORMED FRONTMATTER: {skill}")
    if text.count("\n---\n") < 1:
        print(f"MISSING FRONTMATTER CLOSER: {skill}")
    body = text.split("\n---\n", 1)[1] if "\n---\n" in text else text
    if re.search(r"(?m)^phase:\s*(explore|plan|build|validate|general)\s*$", body):
        print(f"LEAKED PHASE LINE: {skill}")
PY
fi
```

---

## Check 6: Context Budget

Estimate total token footprint per profile:

```bash
if [ -n "$RULES_DIR" ]; then
  echo "=== Rule sizes (lines, approximate token proxy) ==="
  total=0
  for f in $(find "$RULES_DIR" -name "*.md"); do
    lines=$(wc -l < "$f")
    total=$((total + lines))
    echo "  $(basename "$f"): $lines lines"
  done | sort -t: -k2 -rn | head -20
  echo "  TOTAL: $total lines across all rules"
fi
```

Flag if total exceeds 5,000 lines (aggressive context consumption).

---

## Check 7: ADR Numbering

```bash
find docs/decisions -name "*.md" 2>/dev/null | sort
```

Check for gaps in sequential numbering within each category directory.

---

## Output Format

| Check | Status | Issues Found |
|---|---|---|
| Artifact canon | PASS/FAIL | `docs/decisions`, `docs/plans`, `.rune` drift |
| Hook bundle integrity | PASS/WARN/FAIL | Script / metadata / companion / profile / docs drift |
| Rule quality | PASS/WARN/FAIL | Size violations, stale rules, missing structure |
| Orphan rules and skills | PASS/FAIL | Resources not in any profile |
| Cross-references and skill frontmatter | PASS/WARN | Broken links, malformed skills, leaked phase lines |
| Context budget | PASS/WARN | Total lines, oversized rules |
| ADR numbering | PASS/FAIL | Gaps |

Then list specific actions to take, ordered by priority:
1. **Critical** — malformed skills, broken references, stale command or path canon, hook bundle drift
2. **Important** — bloated rules, orphan resources, missing shared doctrine
3. **Advisory** — stale content, budget optimization
