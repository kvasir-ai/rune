---
description: "Audit knowledge base health: documentation hygiene, rule quality, staleness, cross-references, coverage gaps, and context budget. Use after major changes or periodically."
user_invocable: true
---

# Knowledge Base Audit

You are auditing the entire knowledge base for health issues. Run all checks and produce a consolidated report.

## Before You Start

Determine the workspace root and locate the toolkit structure:

```bash
WORKSPACE_ROOT="$(pwd)"

# Find rules directory
RULES_DIR=""
[ -d "src/rules" ] && RULES_DIR="src/rules"
[ -d "ai-toolkit/src/rules" ] && RULES_DIR="ai-toolkit/src/rules"

# Find profiles
PROFILES=""
[ -f "profiles.yaml" ] && PROFILES="profiles.yaml"
[ -f "ai-toolkit/profiles.yaml" ] && PROFILES="ai-toolkit/profiles.yaml"
```

---

## Check 1: Documentation Hygiene

Scan for docs that violate placement policies:

```bash
# Docs inside git repos that should be at workspace root
for repo in $(find . -maxdepth 1 -type d -name "*.git" -o -type d); do
  if [ -d "$repo/.git" ] && [ -d "$repo/docs" ]; then
    echo "=== $repo ==="
    find "$repo/docs/" -name "*.md" -type f 2>/dev/null | head -20
  fi
done
```

Flag ADRs, plans, or design docs found inside repos.

Check CLAUDE.md coverage:
```bash
for repo in $(find . -maxdepth 1 -type d); do
  if [ -d "$repo/.git" ] || [ -f "$repo/pyproject.toml" ] || [ -f "$repo/go.mod" ] || [ -f "$repo/package.json" ]; then
    if [ -f "$repo/CLAUDE.md" ]; then
      echo "$repo: CLAUDE.md present ($(wc -l < "$repo/CLAUDE.md") lines)"
    else
      echo "$repo: MISSING CLAUDE.md"
    fi
  fi
done
```

---

## Check 2: Rule Quality

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

## Check 3: Orphan Rules

Rules that exist in `$RULES_DIR` but are not referenced by any profile:

```bash
if [ -n "$PROFILES" ]; then
  find "$RULES_DIR" -name "*.md" -exec basename {} .md \; | sort > /tmp/all_rules.txt
  grep -oP '^\s+- \K\S+' "$PROFILES" | sort -u > /tmp/profiled_rules.txt
  echo "=== Orphaned rules (not in any profile) ==="
  comm -23 /tmp/all_rules.txt /tmp/profiled_rules.txt
fi
```

---

## Check 4: Broken Cross-References

```bash
if [ -n "$RULES_DIR" ]; then
  grep -rh 'rules/.*\.md' "$RULES_DIR" 2>/dev/null | \
    grep -oP 'rules/[a-z0-9/-]+\.md' | sort -u | while read ref; do
      matches=$(find "$RULES_DIR" -name "$(basename "$ref")" 2>/dev/null | wc -l)
      if [ "$matches" -eq 0 ]; then
        echo "BROKEN: $ref"
      fi
    done
fi
```

---

## Check 5: Context Budget

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

## Check 6: ADR Numbering

```bash
find docs/ -name "ADR-*.md" -o -name "0*.md" 2>/dev/null | sort
```

Check for gaps in sequential numbering within each category directory.

---

## Output Format

| Check | Status | Issues Found |
|---|---|---|
| Documentation hygiene | PASS/FAIL | Details |
| Rule quality | PASS/WARN/FAIL | Size violations, stale rules, missing structure |
| Orphan rules | PASS/FAIL | Rules not in any profile |
| Cross-references | PASS/WARN | Broken links |
| Context budget | PASS/WARN | Total lines, oversized rules |
| ADR numbering | PASS/FAIL | Gaps |

Then list specific actions to take, ordered by priority:
1. **Critical** — broken references, missing CLAUDE.md
2. **Important** — bloated rules, orphans
3. **Advisory** — stale content, budget optimization
