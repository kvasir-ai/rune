Phase: Plan

# DAG Execution Format

> Canonical format for dependency-annotated plans that enable parallel agent dispatch.
> Use when the Planner outputs a plan with 5+ tasks involving 3+ agents.
> See `src/rune-agency/rules/plan/architectural-decision-records.md` for ADR conventions.
> ADR: `docs/decisions/0001-dag-dispatch-for-agent-orchestration.md`

---

## Task Definition

Each task in a DAG plan must have:

```yaml
- id: t1                           # unique within the plan (t1, t2, ...)
  title: "Create user schema"      # human-readable, imperative
  agent: engineer                  # must match a canonical agent name
  depends_on: []                   # list of task IDs (empty = root task)
  output: "migrations/001.sql"     # what this task produces
  files: ["migrations/"]           # files/directories this task will touch
  evidence: ["src/foo/bar.py"]     # sources or predecessor artifacts this task relies on
  assumptions: []                  # what is still assumed rather than proven
  ambiguity: none                  # none | evidence-gap | technical-truth | taxonomy | business
```

### Field Rules

| Field | Required | Constraints |
|---|---|---|
| `id` | Yes | Short alphanumeric (t1, t2, ...). Unique within plan. Never reused. |
| `title` | Yes | Imperative verb phrase. Short. |
| `agent` | Yes | Use the canonical agent identifier from `agent-collaboration.md` (`planner`, `researcher`, `knowledge-manager`, `engineer`, `technical-writer`, `judge`). |
| `depends_on` | Yes | List of task IDs. Empty list `[]` for root tasks. Every ID must exist in the plan. |
| `output` | Yes | What this task produces — files, reports, or changes. Used to describe results to dependent tasks. |
| `files` | Yes | Files/directories this task will read or write. Used for conflict detection. |

### Collaboration Fields

Execution-ready plans should also preserve these fields per task:

| Field | Required | Purpose |
|---|---|---|
| `evidence` | Strongly recommended | Carries source files, briefs, or ledgers forward so downstream agents can verify claims. |
| `assumptions` | Strongly recommended | Prevents hidden uncertainty from disappearing during decomposition. |
| `ambiguity` | Strongly recommended | Classifies unresolved risk so the next agent knows whether to return to Explore, Engineer, or HITL. |

### Canonical Agent Alias Map

Legacy aliases may still appear in older plans. Translate them to canonical names
when rewriting or validating a plan.

| Legacy alias | Canonical name |
|---|---|
| `developer` | `engineer` |
| `specialist` | `engineer` |
| `reviewer` | `judge` |
| `code-reviewer` | `judge` |
| `writer` | `technical-writer` |

---

## Safety Invariants

The DAG execution skill enforces ALL six before any dispatch. If any fails, execution does not begin.

| # | Invariant | How to Check | If Violated |
|---|---|---|---|
| 1 | **Unique IDs** | Every task `id` is unique within the plan | Reject plan. Report duplicate IDs. |
| 2 | **No cycles** | Topological sort succeeds | Reject plan. Report the cycle. Ask user to break it. |
| 3 | **No orphans** | Every task reachable from a root (`depends_on: []`) | Reject plan. Report orphaned tasks. |
| 4 | **No file conflicts** | Two tasks in same wave do not declare overlapping `files` | Move one task to next wave, or ask user to merge tasks. |
| 5 | **All agents valid** | Every `agent` field matches a known agent name | Reject plan. Report invalid agent name. |
| 6 | **All references exist** | Every ID in `depends_on` matches a task `id` | Reject plan. Report dangling reference. |

### If Unsure

If any dependency is ambiguous — you're not sure whether task B truly depends on task A — **add the dependency**. False dependencies are safe (they serialize unnecessarily but produce correct results). Missing dependencies cause race conditions and incorrect results.

If you cannot determine whether a plan is valid, **ask the user** before proceeding.

---

## Wave Computation

Group tasks into waves using topological sort:

```
Wave 0: tasks with depends_on: []           (roots — no prerequisites)
Wave N: tasks whose depends_on are ALL satisfied by waves 0..N-1
```

Tasks in the same wave execute in parallel (multiple Agent calls in one response).

### Example

```yaml
tasks:
  - id: t1, agent: researcher,        depends_on: []
  - id: t2, agent: knowledge-manager, depends_on: []
  - id: t3, agent: planner,           depends_on: [t1, t2]
  - id: t4, agent: engineer,          depends_on: [t3]
  - id: t5, agent: technical-writer,  depends_on: [t3]
  - id: t6, agent: judge,             depends_on: [t4, t5]
```

Waves:
```
Wave 0 (parallel): t1 (researcher), t2 (knowledge-manager)
Wave 1:            t3 (planner)           <- waits for t1, t2
Wave 2 (parallel): t4 (engineer), t5 (technical-writer)
Wave 3:            t6 (judge)             <- waits for t4, t5
```

---

## Parallelism Benefit Estimate

Every DAG plan must include this at the end:

```
Critical path: t1 → t3 → t4 → t6 (4 of 6 tasks, 67%)
Parallelism benefit: 6/4 = 1.5x
Recommendation: DAG dispatch
```

Formula: `benefit = total_tasks / critical_path_length`

## Plan Header Contract

Before the task list, execution-ready plans must include:

- `Scope`
- `Success Criteria`
- `Inputs`
- `Assumptions`
- `Open Questions`
- `Verification`
- `Human Gate`

If a change affects taxonomy, agent names, commands, rule promotion, or public
docs, include explicit governance tasks instead of burying those concerns in
implementation work.

## Sequential Plan Contract

When the work does not justify DAG dispatch, the plan must still preserve the
same cross-phase fields in ordered form.

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
    action: "Confirm runtime behavior"
    output: ".rune/research/runtime-claim.md"
    evidence: ["src/foo.py"]
    ambiguity: evidence-gap
  - order: 2
    owner: planner
    action: "Rewrite the implementation plan"
    output: "docs/plans/2026-04-07-runtime-fix.md"
    evidence: [".rune/research/runtime-claim.md"]
    ambiguity: none
```

Sequential plans use canonical agent IDs, preserve evidence and assumptions,
and still declare a `human_gate`.

---

## When to Use DAG vs Sequential

| Condition | Use DAG | Use Sequential |
|---|---|---|
| 5+ tasks | Yes | — |
| 3+ different agents involved | Yes | — |
| Fan-out pattern (1 task spawns 2+) | Yes | — |
| Critical path < 60% of total tasks | Yes | — |
| Benefit > 1.3x | Yes | — |
| < 4 tasks | — | Yes |
| Linear chain (no parallelism possible) | — | Yes |
| All tasks assigned to same agent | — | Yes |
| Critical path > 70% of total tasks | — | Yes |

If benefit < 1.3x, sequential execution is simpler and nearly as fast. Use the
sequential plan contract instead of forcing a weak DAG.

---

## Context Injection Between Waves

When passing predecessor results to dependent tasks, **summarize — do not dump raw output**.

Each predecessor's result gets 2-3 sentences maximum:
- What was produced (file names, key decisions)
- Any constraints the dependent task must respect
- Any errors or warnings

The dispatcher (main session) does the summarization. This prevents context window bloat across deep DAGs.

---

## Error Handling

| Situation | Response |
|---|---|
| Task fails | Mark task FAILED. Mark all dependents BLOCKED. Ask user: "Continue with remaining unblocked waves?" |
| Task times out | Retry once. If still fails, mark FAILED. |
| Task produces unexpected output | Pause. Show output to user. Ask how to proceed. |
| All tasks in a wave fail | Halt execution. Report to user. |
| User says "skip" a blocked task | Mark SKIPPED. Unblock dependents if they have other satisfied dependencies. |

---

## Integration

| Skill/Agent | Relationship |
|---|---|
| `write-plan` | Produces DAG-annotated plans (when 5+ tasks and 3+ agents) |
| `rune` | Consumes DAG plans, dispatches wave-by-wave |
| `build/execution-contract` | Defines runtime ledger and Build -> Validate handoff requirements |
| `judge-audit` | Post-execution verification after DAG dispatch completes |
| Safety review agent | Pre-gate — validates plan BEFORE DAG execution |

---

## Cross-References

- See `CONTRIBUTING.md` for how to add agents, rules, and skills
- See `rune` skill for the runtime dispatcher
