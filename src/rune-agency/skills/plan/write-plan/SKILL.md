---
description: Generate a strict, atomic, step-by-step implementation plan from a design document or feature request. Optimized for automated execution via /rune.
user_invocable: true
phase: plan
---

# Draft Implementation Plan

Shared contract: apply `src/rune-agency/skills/core/skill-contract/SKILL.md`
before following the phase-specific steps below.

## Overview

Write comprehensive implementation plans assuming the receiving engineer has zero context for the codebase. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

**Announce at start:** "Drafting the implementation plan."

**Tracked plans:** `docs/plans/YYYY-MM-DD-<feature-name>.md`
**Ephemeral plans:** `.rune/plans/<feature-name>.md`

## DAG Annotation (for plans with 5+ tasks and 3+ agents)

When a plan has 5 or more tasks involving 3 or more agents, annotate with dependency metadata. This enables parallel dispatch via `/rune`.

**Add to each task:**
```yaml
- id: t1
  title: "short description"
  agent: agent-name
  depends_on: []
  output: "what this produces"
  files: ["path/pattern"]
  evidence: ["path/or/brief"]
  assumptions: []
  ambiguity: none
```

Use canonical agent names: `planner`, `researcher`, `knowledge-manager`,
`engineer`, `technical-writer`, `judge`.

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

## Task Structure

### Task N: [Component Name]

**Files:**
- Create: `path/to/file`
- Modify: `path/to/existing`
- Test: `path/to/test`

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Write minimal implementation**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit**

## Execution Handoff

After saving the plan: **"Plan complete. Ready to execute? /rune"**
