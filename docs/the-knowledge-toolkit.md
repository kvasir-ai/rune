# The Knowledge Toolkit

> How to teach your agents, manage what they know, and swap context depending on the task.

---

## Three Tools, One Goal

rune has three mechanisms for managing what agents know:

| Tool | What It Does | Command |
|---|---|---|
| **Rules** | Structured knowledge files agents follow | Files in `src/rules/` |
| **Profiles** | Swap which rules are loaded per session | `make use-profile PROFILE=<name>` |
| **Knowledge Manager** | Feeds, shapes, and grows the rule base | `"hey knowledge manager"` |

Together they solve the core problem: AI agents start each session knowing nothing about your project. Without structured knowledge, every session starts from zero.

---

## Rules: What Agents Know

Rules are markdown files in `src/rules/`. They contain conventions, standards, patterns, and reference material. When an agent loads a rule, it follows it — the rule shapes behavior without being explicitly repeated in every prompt.

```
src/rules/
  collaboration/
    design-patterns.md          # Architectural patterns
    project-planning.md         # Planning frameworks
    knowledge-management.md     # How to maintain rules
  engineering/
    ...your domain rules...
```

A good rule is:
- **Actionable** — tells agents what to do, not just what to know
- **Structured** — tables, checklists, code blocks over prose
- **Scoped** — one topic per file, not an encyclopedia

A rule that says "BigQuery supports partitioning" is knowledge. A rule that says "Always partition tables by date. Set `require_partition_filter = true`" is actionable knowledge. The second one changes agent behavior.

---

## Profiles: Focused Context

Profiles select which rules agents load. This is the primary lever for controlling what your team knows.

**Why profiles matter:** Loading every rule into every session wastes context tokens and dilutes focus. A developer writing Go code does not need GDPR compliance rules. A security reviewer does not need CSS conventions. Profiles match knowledge to task.

```yaml
# profiles.yaml
default:
  description: Full engineering — all rules
  rules:
    collaboration:
      - design-patterns
      - project-planning
    engineering:
      - go-conventions
      - python-conventions

security-review:
  description: Security and compliance focus
  rules:
    collaboration:
      - design-patterns
    regulatory:
      - gdpr-compliance
      - threat-modeling
```

### Switching Profiles

```bash
make use-profile PROFILE=default          # full engineering context
make use-profile PROFILE=security-review  # security-focused session
make list-profiles                        # see all available profiles
make show-profile PROFILE=<name>          # preview what a profile loads
```

### Profile Design Principles

- **Lean over complete.** Only include rules the session actually needs. Every rule consumes context tokens.
- **One profile per task type.** A "security review" profile, a "data pipeline" profile, a "frontend" profile.
- **Global rules for universal concerns.** Put git conventions and operational constraints in `global_rules` — they deploy to every profile automatically.
- **Measure your footprint.** Run `make context-budget` to see how many tokens each profile consumes.

### Context Budget

Every token loaded into an agent's context displaces space for reasoning. Most AI frameworks ignore this — they dump everything at startup and hope the model sorts it out.

rune treats context like a budget:

```bash
make context-budget
```

This shows exactly how many tokens each profile consumes. If a profile burns 80K tokens of a 200K window before you even type a question, you have already spent 40% of your budget on overhead.

| Profile | Token Load | % of 200K Window |
|---|---|---|
| `default` | ~45K | 22% |
| `security-review` | ~25K | 12% |
| `data-pipeline` | ~35K | 17% |

The goal is to stay under 25% of the context window for rules — leaving 75%+ for actual work.

---

## Knowledge Manager: Feed, Shape, Grow

The Knowledge Manager is a specialized agent with three jobs:

### Feed: Add New Knowledge

Raw material enters through `src/knowledge/` — the inbox. Drop PDFs, research notes, documentation extracts, or paste content from conversations. The Knowledge Manager reads the inbox and distills it into structured rules.

```
You: "Hey knowledge manager, I dropped a PDF about our new API conventions
      in src/knowledge/. Distill it into a rule."

KM:  Reads the PDF, extracts actionable patterns, creates
     src/rules/engineering/api-conventions.md, registers it in
     profiles.yaml under the relevant profiles.
```

**Never write directly to `src/rules/`.** Always go through `src/knowledge/` first. Raw research has poor signal-to-noise — the Knowledge Manager decides what is actionable, structures it, and promotes it.

### Shape: Maintain Quality

Rules go stale. APIs change, conventions evolve, tools get upgraded. The Knowledge Manager audits the rule base:

```
You: "Audit the knowledge base"

KM:  Checks for stale rules (not updated in 6+ months),
     oversized rules (>800 lines), orphans (not in any profile),
     duplicates, missing cross-references. Reports findings.
```

### Grow: Fill Gaps

When agents are asked questions they cannot answer from existing rules, that topic is a gap. The Knowledge Manager identifies gaps and fills them:

```
You: "Research how GDPR affects our API design and teach the team"

KM:  Searches the web, reads sources, distills findings into a new
     rule in src/rules/regulatory/gdpr-api-design.md. Registers it
     in the security-review profile.
```

---

## The Knowledge Lifecycle

```
Raw material (PDF, research, conversation)
  → src/knowledge/ (inbox — unstructured)
    → Knowledge Manager distills
      → src/rules/{category}/ (structured, deployable)
        → profiles.yaml (assigned to profiles)
          → make use-profile (loaded into agent context)
            → Agent behavior changes
```

Each rotation through this cycle compounds the team's knowledge base. Over time, agents start sessions with increasingly complete domain expertise — not because they remember past conversations, but because the rules they load encode the accumulated learning.
