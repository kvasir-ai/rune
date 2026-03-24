# DAG Execution Format

> Canonical format for dependency-annotated plans that enable parallel agent dispatch.
> Use when the Planner outputs a plan with 5+ tasks involving 3+ agents.
> See `rules/architectural-decision-records.md` for ADR conventions.
> ADR: `docs/decisions/0001-dag-dispatch-for-agent-orchestration.md`

---

## Task Definition

Each task in a DAG plan must have:

```yaml
- id: t1                          # unique within the plan (t1, t2, ...)
  title: "Create user schema"     # human-readable, imperative
  agent: developer                 # must match an agent name in the collective
  depends_on: []                  # list of task IDs (empty = root task)
  output: "migrations/001.sql"    # what this task produces
  files: ["migrations/"]          # files/directories this task will touch
```

### Field Rules

| Field | Required | Constraints |
|---|---|---|
| `id` | Yes | Short alphanumeric (t1, t2, ...). Unique within plan. Never reused. |
| `title` | Yes | Imperative verb phrase. Short. |
| `agent` | Yes | Use the short `subagent_type` name (e.g., `developer`, `architect`, `reviewer`). This is the name used in Agent tool dispatch, NOT the frontmatter `name:` field or the filename. |
| `depends_on` | Yes | List of task IDs. Empty list `[]` for root tasks. Every ID must exist in the plan. |
| `output` | Yes | What this task produces — files, reports, or changes. Used to describe results to dependent tasks. |
| `files` | Yes | Files/directories this task will read or write. Used for conflict detection. |

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
  - id: t1, agent: developer,    depends_on: []
  - id: t2, agent: architect,    depends_on: []
  - id: t3, agent: developer,    depends_on: [t1, t2]
  - id: t4, agent: tester,       depends_on: [t3]
  - id: t5, agent: security,     depends_on: [t3]
  - id: t6, agent: reviewer,     depends_on: [t4, t5]
```

Waves:
```
Wave 0 (parallel): t1 (developer), t2 (architect)
Wave 1:            t3 (developer)      ← waits for t1, t2
Wave 2 (parallel): t4 (tester), t5 (security)
Wave 3:            t6 (reviewer)       ← waits for t4, t5
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

If benefit < 1.3x, sequential execution is simpler and nearly as fast. Use `executing-plans` instead.

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
| `writing-plans` | Produces DAG-annotated plans (when 5+ tasks) |
| `rune` | Consumes DAG plans, dispatches wave-by-wave |
| `executing-plans` | Fallback for non-DAG plans (sequential execution) |
| `dispatching-parallel-agents` | Degenerate case — DAG with no edges (all tasks in Wave 0) |
| Safety review agent | Pre-gate — validates plan BEFORE DAG execution |

---

## Cross-References

- See `CONTRIBUTING.md` for how to add agents, rules, and skills
- See `rune` skill for the runtime dispatcher
