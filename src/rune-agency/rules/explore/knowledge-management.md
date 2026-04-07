Phase: Explore

# Knowledge Management

> Maintaining, auditing, and evolving the Rune Agency rule inventory.
> Also defines when Explore output is ready to hand off into planning or rule
> promotion.

---

## Rule Lifecycle

```
DRAFT → ACTIVE → REVIEW → (UPDATE | ARCHIVE | DELETE)
                    ↑____________________________|
```

| Stage | Definition | Action |
|---|---|---|
| **Draft** | New, not in any profile | Get review, register in a profile |
| **Active** | Deployed, consumed by agents | Periodic review |
| **Review** | Triggered (see below) | Update, split, merge, archive, or delete |
| **Update** | Content revised | Edit in place, redeploy |
| **Archive** | Not needed now, may have future value | Move to the owning phase archive, remove from profiles |
| **Delete** | Redundant, incorrect, or superseded | Delete file, remove from profiles |

## Durable Inputs

Use `src/rune-agency/knowledge/` for durable raw material that may become rules,
profiles, or taxonomy updates later.

Use `.rune/` for ephemeral workflow memory, audits, or scratch packets that
should not become doctrine automatically.

## Explore Output Contracts

Explore work should leave one of these canonical packets behind:

| Packet | Producer | Surface | Minimum fields |
|---|---|---|---|
| Research brief | Researcher | inline response or `.rune/research/<slug>.md` | question, findings, evidence, uncertainties, recommended handoff |
| Context packet | Knowledge Manager | inline response or `.rune/context/<slug>.md` | active profile, loaded rules, terminology constraints, path drift, rule candidates |
| Promotion proposal | Knowledge Manager | `src/rune-agency/knowledge/<slug>.md` | source evidence, proposed doctrine change, affected surfaces, validation command |

Explore is incomplete if it ends as a raw dump of notes with no next owner.

## Explore -> Plan Readiness

Only hand work to Planner when all of these are true:

| Requirement | Fail Action |
|---|---|
| The question is bounded enough to decompose | Keep researching or ask HITL to narrow scope |
| Claims are backed by file paths, commands, or URLs | Route back to Researcher |
| Known contradictions are named, not hidden | Route to Judge or Engineer if technical truth is disputed |
| Path drift or naming drift is surfaced | Route to Knowledge Manager for closure |
| A recommended next owner is explicit | Return the packet and finish the handoff properly |

## Promotion Gate

Do not promote a finding into a rule until all of these are true:

| Check | Fail Action |
|---|---|
| Source evidence exists and is cited | Keep as raw knowledge |
| The behavior change is explicit | Rewrite the proposal before promotion |
| The claim is stable enough to survive reuse | Defer and gather more evidence |
| Technical claims are verified or delegated to Engineer | Route to Engineer |
| Terminology and path impact are known | Route to Knowledge Manager or Technical Writer first |

## Pre-Creation Checklist

| Check | Fail Action |
|---|---|
| One-sentence statement of what agent behavior changes? | Don't create — vague rules waste context |
| No duplicate (`grep -rl "keyword" src/rune-agency/rules/`)? | Extend existing rule |
| Which profiles deploy it? | No profile → don't create |
| Concrete source material available? | Defer until source identified |
| Own file or section in existing rule? | <50 lines → add as section |

## Quality Criteria

| Criterion | Test |
|---|---|
| **Actionable** | Tells agents what to *do*, not just what to know |
| **Structured** | Tables, checklists, code blocks — not prose |
| **Sourced** | Claims attributed: author, year, publication |
| **Scoped** | One coherent topic, no domain sprawl |
| **Current** | Version numbers, APIs, pricing, and commands match the current repo or cited external source |

## Size Guidelines

| Lines | Classification | Action |
|---|---|---|
| < 50 | Minimal | Merge into related rule |
| 50–300 | Lean | Ideal |
| 300–500 | Standard | Acceptable for comprehensive references |
| 500–800 | Heavy | Review for split opportunities |
| > 800 | Bloated | Must split or trim |

## Staleness Detection

Run monthly. Check: (1) rules unmodified 6+ months with version-specific
content, (2) orphan rules not in any profile, (3) size outliers, (4) packets
or docs that still mention `docs/adrs/` or deprecated command families.

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| **Overloaded** (>800 lines) | Split into sub-rules |
| **Stale** (12+ months, version-specific) | Update or archive |
| **Orphaned** (not in any profile) | Add to profile or archive |
| **Duplicate** (two rules, same concept) | Merge into one |
| **Prose-heavy** (paragraphs not tables) | Restructure |
| **Unsourced** (no citation) | Add author, year, publication |
| **Just-in-case** (added speculatively) | Remove — costs context tokens |
| **Isolated** (no cross-references) | Add `## Cross-References` |

## Naming and Organization

**File names:** lowercase kebab-case, no abbreviations (except universal: `api`, `k8s`), descriptive, unique repo-wide.

Rules live under the phase that owns them: `src/rune-agency/rules/<phase>/`.
Only truly shared doctrine belongs under `src/rune-agency/rules/core/`.

## Drift Closure

When path drift, terminology drift, or profile drift is detected:

1. **Knowledge Manager** owns the canonical resolution and rule or profile update.
2. **Engineer** confirms technical reality when the drift affects code, commands, or runtime behavior.
3. **Technical Writer** propagates wording, link, and artifact-path fixes across docs surfaces.
4. **Judge** arbitrates if the surfaces still disagree after attempted repair.

## Archive Process

1. Move to the owning phase archive directory
2. Remove from `profiles.yaml`
3. Remove references from agent headers
4. Add `> ARCHIVED {date}: {reason}` at top
5. Deploy: `rune profile use {active_profile}`

---

## Cross-References

- See `src/rune-agency/rules/core/rune-operations.md` for rule creation, deployment, and profile management
