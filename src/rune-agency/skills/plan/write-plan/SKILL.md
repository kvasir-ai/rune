---
description: Generate a strict, atomic, step-by-step implementation plan from a design document or feature request. Optimized for automated execution via /rune.
user_invocable: true
phase: plan
---

# Draft Implementation Plan

Shared contract: apply `.claude/skills/core/skill-contract/SKILL.md`
before following the phase-specific steps below.

## Overview

Write comprehensive implementation plans assuming the receiving engineer has zero context for the codebase. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

**Announce at start:** "Drafting the implementation plan."

**Tracked plans:** `docs/plans/YYYY-MM-DD-<feature-name>.md`
**Ephemeral plans:** `.rune/plans/<feature-name>.md`

## Planning Principles

- Model the workflow, not the implementation diary. A plan should describe what must happen, in what order, by whom, and what each step produces.
- Keep topology stable. Only introduce parallel waves when tasks are truly independent in files, evidence, and blocking decisions.
- Make roots obvious. A good plan starts with the smallest set of prerequisite tasks that unlock the rest of the work.
- Make joins explicit. If two branches must reconverge for validation, integration, or docs updates, represent that as its own task.
- Preserve evidence and uncertainty. Do not collapse research, assumptions, or unresolved questions into vague implementation bullets.
- Treat verification as first-class work. Tests, validation commands, docs regeneration, and review gates belong in the plan rather than in a closing sentence.
- Represent governance work explicitly. If the change affects rules, skills, agents, hooks, docs, ADRs, or naming, create dedicated tasks for those surfaces.

## Choose the Plan Shape

Use a DAG when the work has multiple roots, meaningful fan-out, or a validation join. Use a sequential plan when the work is essentially one chain.

### Prefer a DAG when

- 5 or more tasks are required
- 3 or more agents are involved
- one task unlocks two or more independent branches
- verification or documentation must wait on multiple implementation branches
- the critical path is much shorter than the total task count

### Prefer a sequential plan when

- the work is one straight line
- the same agent owns nearly every step
- there is little or no safe parallelism
- dependency annotations would add noise rather than clarity

## Plan Template

Start every plan with this header, then choose either the DAG template or the sequential template.

```markdown
# <Plan Title>

## Scope
- In:
- Out:

## Success Criteria
- "<observable outcome>"
- "<validation outcome>"

## Inputs
- "<ticket, brief, path, prior decision>"

## Assumptions
- "<assumption>"

## Open Questions
- "<question or 'None'>"

## Verification
- "<command or review step>"

## Human Gate
- GO | WAIT | STOP
- Reason: "<why this gate is correct>"
```

### DAG Template

Use this when the plan benefits from parallel dispatch via `/rune`.

When a plan has 5 or more tasks involving 3 or more agents, annotate with dependency metadata. This enables parallel dispatch via `/rune`.

```yaml
tasks:
  - id: t1
    title: "Produce the missing context"
    agent: researcher
    depends_on: []
    output: ".rune/research/<topic>.md"
    files: ["src/path", "docs/path"]
    evidence: ["ticket", "src/path"]
    assumptions: []
    ambiguity: evidence-gap

  - id: t2
    title: "Implement the code change"
    agent: engineer
    depends_on: [t1]
    output: "working implementation + tests"
    files: ["src/module.py", "tests/test_module.py"]
    evidence: [".rune/research/<topic>.md"]
    assumptions: []
    ambiguity: technical-truth

  - id: t3
    title: "Update the durable docs"
    agent: technical-writer
    depends_on: [t2]
    output: "updated docs source"
    files: ["README.md", "src/cli/site/**"]
    evidence: ["src/module.py", ".rune/research/<topic>.md"]
    assumptions: []
    ambiguity: none

  - id: t4
    title: "Validate the finished change"
    agent: judge
    depends_on: [t2, t3]
    output: ".rune/reviews/<topic>.md"
    files: [".rune/reviews/"]
    evidence: ["tests", "docs", "implementation diff"]
    assumptions: []
    ambiguity: none
```

Then add:

```markdown
## Critical Path
- `t1 -> t2 -> t4`

## Parallelism Benefit
- `4 / 3 = 1.3x`

## Recommendation
- DAG dispatch
```

### Sequential Template

Use this when the work is linear and a DAG would be performative.

```yaml
scope: "..."
success_criteria:
  - "..."
inputs:
  - "..."
assumptions:
  - "..."
open_questions:
  - "..."
verification:
  - "..."
human_gate: GO | WAIT | STOP
steps:
  - order: 1
    owner: researcher
    action: "Confirm the current behavior and affected paths"
    output: ".rune/research/<topic>.md"
    evidence: ["src/path"]
    ambiguity: evidence-gap
  - order: 2
    owner: engineer
    action: "Implement the change and prove it"
    output: "code + tests"
    evidence: [".rune/research/<topic>.md"]
    ambiguity: technical-truth
  - order: 3
    owner: judge
    action: "Review the final behavior and verification"
    output: ".rune/reviews/<topic>.md"
    evidence: ["test output", "diff"]
    ambiguity: none
```

## Task Patterns

Use these patterns to keep plans readable and dispatchable.

### Root Task

Use for prerequisite research, schema inspection, or current-state confirmation.

```yaml
- id: t1
  title: "Confirm current behavior"
  agent: researcher
  depends_on: []
  output: ".rune/research/current-state.md"
  files: ["src/path"]
  evidence: ["ticket", "src/path"]
  assumptions: []
  ambiguity: evidence-gap
```

### Fan-Out Task

Use when one confirmed prerequisite unlocks two or more independent branches.

```yaml
- id: t3
  title: "Implement runtime change"
  agent: engineer
  depends_on: [t1]
  output: "runtime update"
  files: ["src/runtime.py"]
  evidence: [".rune/research/current-state.md"]
  assumptions: []
  ambiguity: none

- id: t4
  title: "Update docs and onboarding copy"
  agent: technical-writer
  depends_on: [t1]
  output: "docs update"
  files: ["README.md", "src/cli/site/**"]
  evidence: [".rune/research/current-state.md"]
  assumptions: []
  ambiguity: none
```

### Join Task

Use when multiple branches must reconverge before the work can ship.

```yaml
- id: t5
  title: "Validate integrated behavior"
  agent: judge
  depends_on: [t3, t4]
  output: ".rune/reviews/integration.md"
  files: [".rune/reviews/"]
  evidence: ["implementation diff", "docs diff", "test output"]
  assumptions: []
  ambiguity: none
```

### Governance Task

Use when the change alters shared doctrine, naming, profiles, hooks, or public docs.

```yaml
- id: t6
  title: "Align shared rule and docs surfaces"
  agent: knowledge-manager
  depends_on: [t3]
  output: "updated rule or profile guidance"
  files: [".claude/rules/", "profiles.yaml", "AGENTS.md"]
  evidence: ["implementation diff"]
  assumptions: []
  ambiguity: taxonomy
```

Before the task list, include:
- `Scope`
- `Success Criteria`
- `Inputs`
- `Assumptions`
- `Open Questions`
- `Verification`
- `Human Gate`

When the work does not justify a DAG, use a sequential plan contract instead of
forcing dependency annotations:

```yaml
scope: "..."
success_criteria:
  - "..."
inputs:
  - "..."
assumptions:
  - "..."
open_questions:
  - "..."
verification:
  - "..."
human_gate: GO | WAIT | STOP
steps:
  - order: 1
    owner: researcher
    action: "..."
    output: ".rune/research/example.md"
    evidence: ["src/path"]
    ambiguity: evidence-gap
```

If the change affects docs, taxonomy, rules, or ADRs, represent that as
explicit governance work instead of hiding it in implementation steps.

If the change affects hooks, represent hook work explicitly:

- hook script changes
- `hooks-meta.yaml` changes
- companion config changes
- profile hook wiring changes
- runtime docs or generated site updates

## Authoring Heuristics

- Prefer one owner per task. Shared ownership usually means the task is underspecified.
- Prefer outputs over intentions. `output` should name the artifact, verification, or state change the next task will consume.
- Prefer explicit joins over magical completion. If final review needs code and docs, make both dependencies visible.
- Prefer fewer, stronger tasks over verbose micro-steps. A plan is a dispatch artifact, not a keystroke transcript.
- Prefer stable file scopes. If two parallel tasks touch the same file, they probably do not belong in the same wave.
- Prefer evidence-carrying tasks early. The sooner the plan captures truth, the less rework later waves need.

## Execution Handoff

After saving the plan: **"Plan complete. Ready to execute? /rune"**
