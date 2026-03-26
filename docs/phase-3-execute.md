# Phase 3: Execute

> Dispatch the plan in parallel waves. Each wave's results are summarized into the next wave's prompts. A Judge verifies at the end.

---

## How Execution Works

The DAG dispatcher takes the plan and executes it wave by wave:

1. **Wave 0**: Dispatch independent tasks in parallel (multiple Agent calls in one response)
2. **Collect results**: Each agent returns a summary of what it built
3. **Inject context**: Summarize Wave 0 results into Wave 1 prompts (2-3 sentences per predecessor — never dump raw output)
4. **Wave 1**: Dispatch dependent tasks with context from predecessors
5. **Repeat** until all waves complete
6. **Report**: Show token usage, cost, and time saved

---

## Use rune

Type `/rune` to dispatch a plan. The dispatcher validates the DAG, computes waves, and executes.

After execution, use `/judge` to review the output, or `/judge-audit` for a deep adversarial audit. For high-stakes changes, `/judge-panel 3` summons independent reviewers for multi-perspective validation.

When the work is ready to ship, `/tw-draft-pr` drafts the PR description and `/tw-release` prepares the release.

---

## Inter-Wave Context Injection

Wave 0 completes. Each agent returns a short summary:

```
#1 (DEVELOPER):  "Created internal/handler/retirement.go with POST /v1/retirement.
                  Accepts JSON body. Returns 200 OK.
                  Added route registration in server/routes.go."

#2 (DEVELOPER):  "Created src/calc/l19_retirement.py with
                  compute_l19(personal, financial, scenario_params).
                  Added to orchestrator call chain. All existing tests pass."
```

The dispatcher summarizes these into the Wave 1 prompt for #3:

```
Predecessor results:
- #1 created POST /v1/retirement in internal/handler/retirement.go.
  Accepts JSON, returns 200. Route registered in server/routes.go.
- #2 created compute_l19() in src/calc/l19_retirement.py.
  Function signature: compute_l19(personal, financial, scenario_params).

Your task: Wire the endpoint to the calculation backend.
```

Task #3 receives exactly what it needs — the endpoint shape from #1 and the function signature from #2 — without seeing the hundreds of lines of code that were written. This is context injection, not context dumping.

---

## Validation

Six safety checks run before anything dispatches. All six must pass.

| Check | What It Catches |
|---|---|
| Unique IDs | Two tasks with the same `id` |
| No cycles | t1 depends on t3, which depends on t1 |
| No orphans | A task that nothing can reach |
| No file conflicts | Two parallel tasks writing to the same directory |
| Valid agents | An `agent` field that does not match any deployed agent |
| Valid references | A `depends_on` pointing to a task ID that does not exist |

If any check fails, `/rune` stops and tells you what is wrong. It does not guess. It does not proceed with a partial plan.

---

## Error Handling

If a task fails, all dependent tasks are automatically blocked. The dispatcher reports the failure and presents three options: retry the failed task, skip it and continue with unblocked tasks, or halt entirely. The human decides — agents never silently swallow failures.

---

## Ad-Hoc Dispatch

You do not always need a formal plan. Sometimes you want three opinions on the same question.

```
You: "I need perspectives on whether to use WebSockets or SSE. /rune"
```

rune constructs a DAG on the fly — three independent assessments feeding into one Judge synthesis. No YAML. No plan file. The dispatcher identifies that parallel work feeds into a convergence step, builds the implicit DAG, and dispatches it.

---

## Token Economics

Every dispatch ends with a cost report:

```
───────────────────────────────────────────
  💰 Token Economics
───────────────────────────────────────────
  t1  developer       322K tok   $6.76
  t2  developer       394K tok   $8.28
  t3  reviewer        304K tok   $6.38
───────────────────────────────────────────
  Total tokens:  1,020K
  Est. cost:     $21.42
  Wall time:     6m 12s  (parallel)
  CPU time:      14m 30s (sequential sum)
  Time saved:    57% via parallelism
───────────────────────────────────────────
```

Cost visibility before dispatch. Cost tracking after. No surprises.

---

## History and Recovery

Every `/rune` dispatch is saved to `.rune/` in the project root. Each file contains the full plan, wave assignments, per-task results, and token economics.

If a session dies mid-dispatch, the history file shows which tasks completed. Resume by running `/rune` with "resume from .rune/{filename}" — rune reads the file, skips completed tasks, and picks up where it left off.

The `.rune/` directory is gitignored by default. If you want audit trails in version control, remove the gitignore entry.

---

## When NOT to Use Multi-Agent Dispatch

| Situation | Just Do It Directly |
|---|---|
| Single-file bug fix | One agent, main conversation |
| Quick config change | No planning needed |
| Question about the codebase | Direct search or Explore agent |
| Task fully within one agent's domain | No handoff needed |

**The threshold:** If the task touches one file in one domain, do it directly. If it touches multiple files across multiple domains, plan and dispatch.

---

## The Synergy

```
Specialization    Each agent carries only the knowledge it needs
     +            → Lower per-agent token cost
Planning          Tasks decomposed with explicit dependencies
     +            → No wasted effort, no rework
DAG Dispatch      Independent tasks run simultaneously
     =            → Same total tokens, much less wall time
                  → Better quality (specialists > generalists)
                  → Auditable (every task tracked with cost)
```

The three ideas reinforce each other:
- **Without specialization**, parallel dispatch is just running the same generalist multiple times
- **Without planning**, agents duplicate work and create merge conflicts
- **Without DAG dispatch**, a good plan still executes sequentially

Together, they produce work that is faster, cheaper, and higher quality than any single approach alone.

---

*Previous: [Phase 2: Plan](phase-2-plan.md). Start over: [Phase 1: Explore](phase-1-explore.md).*
