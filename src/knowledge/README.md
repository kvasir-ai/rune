# Knowledge Inbox

Raw material and archived knowledge that is NOT deployed to agent context windows. This is the staging area where unstructured content lands before the Knowledge Manager distills it into active rules.

---

## The Pipeline

```
Raw material (PDF, paper, research, web extract)
  --> src/knowledge/ (inbox -- raw or lightly structured)
    --> Knowledge Manager distills
      --> src/rules/{category}/ (active -- deployed to agent context)
```

**Never skip the inbox.** Dropping raw material directly into `src/rules/` pollutes agent context with unstructured content that consumes tokens without improving agent behavior.

---

## Two Purposes

1. **Inbox** -- raw ingested material waiting to be distilled into focused, actionable rules
2. **Archive** -- rules that were once active but have been trimmed during an audit (too generic, too large, superseded)

---

## Worked Example

You have a 40-page PDF describing your team's API conventions.

**Step 1: Extract and park in the inbox**

```bash
# Parse the PDF
uv tool run --from PyMuPDF python3 -c "
import fitz
doc = fitz.open('api-conventions.pdf')
for i in range(len(doc)):
    print(doc[i].get_text())
" > src/knowledge/api-conventions-raw.txt
```

Add a header to the file:

```markdown
> INBOX: 2026-03-23 -- API conventions extracted from team PDF.
> Source: api-conventions.pdf (40 pages, internal document)

[... extracted text ...]
```

**Step 2: Knowledge Manager distills**

The Knowledge Manager reads the inbox file, identifies the actionable content (naming conventions, error response patterns, authentication requirements), and creates a focused rule:

```bash
# Knowledge Manager creates:
src/rules/engineering/api-conventions.md    # 200 lines, tables + checklists
```

**Step 3: Register and deploy**

Add the new rule to the appropriate profile in `profiles.yaml`, then deploy:

```bash
make use-profile PROFILE=default
```

The raw 40-page extract stays in `src/knowledge/` for reference. The distilled 200-line rule goes into agent context.

---

## What Goes Here vs What Goes in Rules

| Content Type | Location | Why |
|---|---|---|
| Raw research output (long, unstructured) | `src/knowledge/` | Too noisy for agent context -- needs distillation |
| PDF extracts, paper summaries | `src/knowledge/` | Source material, not agent-ready |
| Archived rules (trimmed during audit) | `src/knowledge/` | Valuable for humans, not for token budgets |
| Source material for future rules | `src/knowledge/` | Parked until needed |
| Actionable, structured knowledge | `src/rules/` | Ready for agents -- tables, checklists, code blocks |
| Decision tables that constrain behavior | `src/rules/` | Must be in agent context to be followed |

---

## Conventions

- **Inbox files**: mark with `> INBOX: {date} -- {topic}` at the top
- **Archived files**: mark with `> ARCHIVED {date}: {reason}` at the top. Preserve the original filename for traceability.
- **No frontmatter** -- plain markdown, same as rules
- **No deployment** -- nothing in this directory is registered in `profiles.yaml`

---

## Cross-References

- See `src/rules/collaboration/ai-toolkit-operations.md` for the full knowledge lifecycle
- See `src/rules/collaboration/knowledge-management.md` for rule quality criteria and audit processes
