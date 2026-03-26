# Architectural Decision Records (ADRs)

> Enshrining design decisions as immutable, version-controlled records.
> Sources: Michael Nygard (2011), MADR 4.0, EDPB WP248, Spotify Engineering, AWS Prescriptive Guidance, Azure Well-Architected Framework, ThoughtWorks Radar, Zimmermann (2023).
> Use when making, reviewing, or discovering architectural decisions.

---

## What Is an ADR

A short document capturing one architecturally significant design decision, its context, and its consequences. ADRs solve the problem of decisions lost in Slack, meetings, and tribal knowledge.

| Property | Value |
|---|---|
| Scope | One decision per ADR |
| Length | 1-2 pages maximum |
| Mutability | Immutable after acceptance — supersede, never edit |
| Storage | Source control, next to the code — never a wiki |
| Audience | Current and future team members, AI coding agents |

---

## When to Write an ADR

| Trigger | Action |
|---|---|
| Choosing a framework, library, or tool | Write ADR |
| Defining API contracts or data formats | Write ADR |
| Selecting deployment strategy or infrastructure pattern | Write ADR |
| Making a security-critical or compliance-critical choice | Write ADR |
| Choosing between competing architectural patterns | Write ADR |
| Decision spans multiple teams or repos | Write RFC first, then ADR |
| Routine, easily reversible choice | Skip ADR |
| Already covered by existing policy or rule | Skip ADR |

Rule of thumb: the cost of documenting is small compared to the cost of an undocumented decision being revisited.

---

## Agent Execution Requirements

**ADR work must always be performed by an opus subagent (1M context).** ADRs require deep reasoning about architectural trade-offs, cross-system consequences, and compliance implications. The opus model's extended context window ensures the agent can hold the full codebase context, existing ADRs, and regulatory requirements simultaneously.

| Task | Required Model | Rationale |
|---|---|---|
| Writing a new ADR | **opus** | Must reason about all existing ADRs, system architecture, and consequences |
| Reviewing/validating an ADR | **opus** | Must cross-reference regulatory rules and project constraints |
| Checking ADR compliance before a code change | **opus** or **sonnet** | Sonnet acceptable for simple compliance checks; opus for ambiguous cases |
| Superseding an existing ADR | **opus** | Must understand the full decision history and impact chain |

When dispatching subagents for ADR work, always set `model: "opus"` in the Agent tool invocation. Multiple ADR tasks may run in parallel — each as a separate opus subagent.

---

## ADR vs RFC vs Design Doc

| Document | Purpose | Timing | Scope | Mutability |
|---|---|---|---|---|
| **RFC** | Solicit feedback on an open question | Before decision | Broad — problem space, options | Mutable during discussion |
| **ADR** | Record a decision and its rationale | At or after decision | Narrow — one specific decision | Immutable after acceptance |
| **Design Doc** | Detailed implementation specification | Before/during implementation | Deep — how to implement | Mutable, living document |

Natural workflow: RFC (debate) → ADR (record conclusion) → Design Doc (detail implementation). Small decisions skip RFC. Routine implementation skips ADR.

---

## Template: MADR 4.0 (Recommended)

Use MADR (Markdown Any Decision Records) as the default template. Dual-licensed MIT/CC0. 2.1k GitHub stars. Most widely adopted extended format.

```markdown
---
status: {proposed | accepted | deprecated | superseded by [ADR-NNNN](NNNN-title.md)}
date: YYYY-MM-DD
decision-makers: [list]
consulted: [list]
informed: [list]
---

# NNNN: Title (short problem/solution summary)

## Context and Problem Statement

2-3 sentences describing the problem and the forces at play.

## Decision Drivers

- Driver 1
- Driver 2

## Considered Options

1. Option A
2. Option B
3. Option C

## Decision Outcome

Chosen option: "Option B", because {justification linking back to decision drivers}.

### Consequences

- Good, because ...
- Good, because ...
- Bad, because ...

### Confirmation

How to validate this was implemented correctly (e.g., test, design review, metric).

## Pros and Cons of the Options

### Option A

- Good, because ...
- Bad, because ...

### Option B

- Good, because ...
- Neutral, because ...
- Bad, because ...

### Option C

- Good, because ...
- Bad, because ...

## More Information

Links to related ADRs, design docs, RFCs, or external references.
```

### Minimal Variant (for small decisions)

```markdown
---
status: accepted
date: YYYY-MM-DD
---

# NNNN: Title

## Context and Problem Statement

[Problem description]

## Decision Outcome

Chosen option: "[option]", because [justification].

### Consequences

- Good, because ...
- Bad, because ...
```

### Y-Statement Format (for inline/quick capture)

For commit messages, PR descriptions, or early-stage capture before a full ADR:

> "In the context of **{use case}**, facing **{concern}**, we decided for **{option}** and neglected **{other options}**, to achieve **{system qualities}**, accepting **{downside}**, because **{rationale}**."

---

## Status Lifecycle

```
Proposed --> Accepted --> [unchanged until...]
    |                          |
    +--> Rejected         Superseded by ADR-NNNN
                               |
                          Deprecated (if no replacement)
```

| Status | Meaning | Can Modify Content? |
|---|---|---|
| Proposed | Under review, open for comments | Yes |
| Accepted | Approved, in effect | No — immutable |
| Rejected | Considered and declined | No — immutable |
| Deprecated | No longer relevant (context changed) | Add deprecation note only |
| Superseded | Replaced by a newer ADR | Add "superseded by" link only |

### How to Supersede

1. Write a new ADR with the next sequential number
2. In the new ADR's Context, reference the old ADR and explain what changed
3. Update the old ADR's YAML frontmatter status only: `superseded by [ADR-NNNN](NNNN-title.md)`
4. Do not modify any other content in the old ADR

### Review Before Acceptance

ADRs should be reviewed by a qualified team member or the Reviewer agent before acceptance. The reviewer's role is to surface risks, contradictions, and gaps — the human (user) is the sole authority for accepting, rejecting, or superseding ADRs.

---

## Directory Structure and Naming

### Location

**Platform-wide ADRs** go in `docs/decisions/` organized by category:

```
docs/decisions/
  infrastructure/   # Cloud infrastructure, IaC, networking, deployment
  data/             # Data pipelines, schema design, storage decisions
  api/              # API contracts, identity, authentication, OpenAPI
  security/         # threat models, access control, compliance
  governance/       # data quality, PII classification, retention
```

**Service-specific ADRs** go in `docs/decisions/` within each repository:

```
{repo}/
  docs/
    decisions/
      0001-use-postgresql-for-persistence.md
      0002-adopt-event-sourcing-for-orders.md
```

Use "decisions" not "adr" — teams report higher adoption when the term is demystified.

Plans go in `docs/plans/` (mutable working documents). ADRs go in `docs/decisions/` (immutable once accepted). These are complementary: a plan may reference multiple ADRs, and an ADR may be created during the planning process.

### File Naming

**4-digit zero-padded sequential number + kebab-case title:**

```
0001-use-react-for-frontend.md
0002-choose-postgres-over-dynamodb.md
0003-adopt-option-a-identity-strategy.md
```

Numbers are never reused. If ADR-0005 is superseded, the replacement is the next number in sequence.

### Monorepo vs Per-Repo

| Approach | When |
|---|---|
| Per-repo ADRs | Decisions scoped to one service/component |
| Centralized ADRs | Cross-cutting decisions (shared infra, org-wide standards) |
| Hybrid | Both — cross-cutting in platform repo, service-specific in each service |

### Cross-Repo References

Reference by relative path or URL:
```markdown
See [PLATFORM-0003](https://github.com/org/platform/blob/main/docs/decisions/0003-shared-auth.md)
```

---

## Anti-Patterns (Ozimmer, 2023)

| Anti-Pattern | What Goes Wrong |
|---|---|
| **Fairy Tale** | Only presents benefits, ignores trade-offs |
| **Sales Pitch** | Marketing language, adjectives without evidence |
| **Free Lunch Coupon** | Documents only harmless consequences, hides downsides |
| **Dummy Alternative** | Presents obviously unworkable options to favor the preferred choice |
| **Sprint** | Only one option considered, only short-term effects discussed |
| **Tunnel Vision** | Ignores stakeholders beyond the immediate team |
| **Mega-ADR** | Multiple pages of architecture specs — should be a design doc |
| **Blueprint in Disguise** | Reads like a cookbook, not a decision journal |

### Quality Checklist

Before accepting an ADR, verify:

- [ ] States the problem clearly in 2-3 sentences
- [ ] Lists at least 2 genuine alternatives (no dummy options)
- [ ] Documents both positive AND negative consequences
- [ ] Consequences section is non-empty — an ADR without consequences is just a status update
- [ ] Stays under 2 pages — if longer, split into ADR + design doc
- [ ] Uses active voice: "We will..." not "It was decided that..."
- [ ] References related ADRs if this supersedes or depends on prior decisions

---

## ADRs and AI/LLM Agents

ADRs are high-value context for AI coding agents because they answer "why" — information that code alone cannot provide.

### How ADRs Help AI Agents

- Agent encounters `0007-use-postgresql-over-dynamodb.md` → understands why PostgreSQL was chosen → avoids suggesting DynamoDB
- "Considered Options" sections prevent agents from recommending alternatives already evaluated and rejected
- Structured format (Context → Decision → Consequences) maps directly to what agents need for contextually appropriate suggestions
- ADRs constrain the solution space, reducing hallucination

### Using AI to Draft ADRs

Effective pattern from Equal Experts:
1. Provide a brief decision statement to the LLM
2. LLM expands into full MADR-format ADR
3. Team shifts from writing to **reviewing and arguing**
4. Use a different LLM (e.g., the Reviewer agent) to critique the draft before human review

Mitigations required:
- LLMs hallucinate references and API features — fact-check every link
- Explicitly instruct: "Do not fabricate product features or external references"
- Treat LLM output as a first draft, never a final record

### ADRs in llms.txt

Include ADRs in `llms.txt` and `llms-full.txt` for AI discoverability:
```markdown
## Architecture Decisions

- [ADR-0001: Use PostgreSQL](docs/decisions/0001-use-postgresql.md): Chose PostgreSQL over DynamoDB for ACID transactions
- [ADR-0003: Option A Identity Strategy](docs/decisions/0003-identity-strategy.md): Opaque external_person_id, no structured identifiers in MVP
```

---

## Tooling (Liberal Licenses)

| Tool | Language | License | Use For |
|---|---|---|---|
| **MADR templates** | Markdown | MIT/CC0 | Template files — full, minimal, bare variants |
| **Log4brains** | TypeScript | Apache 2.0 | Web UI, timeline, search, CI/CD publishing |
| **ADG** | Go | Apache 2.0 | CLI for creating/managing ADRs, recurring decision models |
| **pyadr** | Python | MIT | Full lifecycle management (propose, accept, reject, deprecate, supersede) |

Note: `adr-tools` (Nygard's original) is GPL — avoid in MIT/Apache-only environments.

---

## Cross-References

- See `rules/design-patterns.md` for architectural patterns that ADRs often reference
- See `rules/knowledge-management.md` for how ADRs relate to the broader knowledge base
