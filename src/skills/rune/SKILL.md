---
description: Execute DAG-annotated plans OR ad-hoc parallel dispatches with wave-based visualization. Use when dispatching 2+ agents — whether from a formal plan with depends_on fields, or an improvised research/opinion fan-out. Always shows the dispatch diagram before execution. Computes waves via topological sort, dispatches independent tasks in parallel, collects results, and injects context into dependent tasks.
user_invocable: true
---

# Executing DAG Plans

## Overview

Execute a DAG-annotated plan by dispatching agents in parallel waves. Each wave contains tasks whose dependencies are all satisfied. Tasks within a wave run simultaneously via multiple Agent calls in a single response.

**Announce at start:** "I'm using the rune skill. Validating DAG before execution."

**Plan source identification:** Determine where the plan came from:
- If executing a plan from a file (e.g., `PLAN.md`, `docs/plans/feature-x.md`), record the file path as the plan source
- If executing a plan produced by the `write-plan` skill in this session, record `write-plan (session)`
- If constructing an ad-hoc DAG from a user prompt, record `ad-hoc`

Include the plan source in the dispatch header and history file.

**Prerequisites:**
- Plan must have tasks with `id`, `agent`, `depends_on`, `output`, and `files` fields
- See `rules/dag-execution-format.md` for the canonical format
- For plans WITHOUT DAG annotations, use sequential execution instead

## Ad-Hoc Parallel Dispatch (No Pre-Existing DAG)

When invoked for research, opinion-gathering, or exploratory tasks that don't have a formal DAG plan:

1. **Always show the dispatch diagram** — even for ad-hoc parallel dispatches. The visual plan is mandatory regardless of whether the task is a formal DAG or an improvised parallel fan-out.
2. **Construct an implicit DAG on the fly** — assign task IDs (t1, t2...), identify agents, determine parallelism, and display the standard dispatch diagram.
3. **Proceed immediately after showing the diagram** — do NOT ask "proceed? (y/n)" for ad-hoc dispatches. The user invoked the skill; that is the authorization.
4. **Include a Judge in the final wave** — ad-hoc dispatches should always end with a Judge synthesizing the parallel results.

**Format for ad-hoc dispatch diagram:**

```
───────────────────────────────────────────
  AD-HOC PARALLEL DISPATCH
  Agents: 4  |  Waves: 2  |  Type: research
  Plan: ad-hoc
───────────────────────────────────────────

  Wave 0  ─── parallel (fan-out) ─────────
  ⚙️  t1  developer            Assess from backend perspective
  🔍  t2  researcher           Assess from documentation perspective
  🔒  t3  security             Assess from compliance perspective
  🧪  t4  tester               Run test coverage analysis

  Wave 1  ────────────────────────────────
  🔍  t5  reviewer             Synthesize all perspectives
                                 ↳ depends on: t1, t2, t3, t4

───────────────────────────────────────────
```

This applies to ANY multi-agent dispatch — formal DAG plans, research questions, opinion-gathering, or brainstorming. The diagram is the universal pre-execution artifact.

## Step 1: Validate the DAG

Before any execution, check ALL six safety checks. If ANY fails, STOP and report.

```
For each task in the plan:
  1. Does `id` exist and is it unique?
  2. Does `agent` match a known agent name?
  3. Do all IDs in `depends_on` exist as task IDs in this plan?
  4. Are there any cycles? (Can you sort all tasks into waves without getting stuck?)
  5. Are there tasks with no path from a root? (orphans)

For each wave (after computing waves):
  6. Do any two tasks in the same wave declare overlapping `files`?
```

**If validation fails**, display a formatted error and stop:

```
───────────────────────────────────────────
  ❌ DAG VALIDATION FAILED
───────────────────────────────────────────
  Invariant 1: CYCLE DETECTED
  Tasks involved: t3 → t5 → t3

  Fix the cycle and retry, or execute
  sequentially.
───────────────────────────────────────────
```

Do NOT proceed. Ask the user to fix and retry.

**If validation passes:**
- Display: "DAG validated. N tasks, M waves, critical path: X tasks (Y%), benefit: Z.Zx"

## Step 2: Compute Waves and Display Pre-Dispatch Report

```
Wave 0 = tasks where depends_on is empty
Wave N = tasks where ALL depends_on tasks are in waves 0..N-1
```

Display the wave plan as a **visually formatted dispatch report**. Use the emoji from each agent's frontmatter. If an agent has no emoji, use the default robot emoji.

**Agent emoji lookup** (from agent frontmatter `emoji:` field):

| Agent | Emoji | Fallback |
|---|---|---|
| developer | ⚙️ | |
| researcher | 🔍 | |
| reviewer | 🔍 | |
| tester | 🧪 | |
| architect | 🏗️ | |
| writer | ✍️ | |
| designer | 🎨 | |
| devops | 🚀 | |
| security | 🔒 | |
| planner | 🗺️ | |
| judge | ⚖️ | |
| knowledge-manager | 📚 | |
| technical-writer | ✍️ | |
| *(unknown agent)* | 🤖 | Default |

**Format the pre-dispatch report like this:**

```
───────────────────────────────────────────
  DAG DISPATCH PLAN
  Tasks: 6  |  Waves: 4  |  Benefit: 1.5x
  Plan: docs/plans/api-feature.md
───────────────────────────────────────────

  Wave 0  ─── parallel ───────────────────
  ⚙️  t1  developer            Define API schemas
  🏗️  t2  architect            Create database migration

  Wave 1  ────────────────────────────────
  ⚙️  t3  developer            Implement API handlers
                                 ↳ depends on: t1, t2

  Wave 2  ─── parallel ───────────────────
  🧪  t4  tester               Write integration tests
                                 ↳ depends on: t3
  🔒  t5  security             Security review
                                 ↳ depends on: t3

  Wave 3  ────────────────────────────────
  🔍  t6  reviewer             Final code review
                                 ↳ depends on: t4, t5

───────────────────────────────────────────
  Critical path: t1 → t3 → t4 → t6
  Path length: 4 of 6 tasks (67%)
───────────────────────────────────────────
```

Ask user: "Proceed with this execution plan? (y/n)"

## Step 3: Execute Wave by Wave

For each wave, in order:

### 3a. Announce the wave

Display a compact dispatch banner with agent emojis. Execution banners use `═══` (double line) to visually distinguish live execution from planning (`───` light line). Both are 43 characters wide.

```
═══ Wave 0: Dispatching 2 agents ══════════
  ⚙️  t1 → developer          Define API schemas
  🏗️  t2 → architect          Create database migration
═══════════════════════════════════════════
```

The `→` arrow between task ID and agent name appears ONLY in execution banners — it signals "action happening now." Pre-dispatch and final report omit it.

Use the emoji from the agent's frontmatter `emoji:` field. If the agent is not in the lookup table, check the frontmatter. If no emoji exists, use 🤖.

### 3b. Construct agent prompts

For each task in the wave, build a prompt containing:
1. The task title and description from the plan
2. **Summarized results from predecessors** (2-3 sentences each, NOT raw output)
3. The files this task should touch (from `files` field)
4. Constraint: "You may ONLY touch files listed in your task scope: [files list]. If you need to modify a file NOT in your scope, STOP immediately and report back — do not modify it."
5. Constraint: "Return a summary of what you did, what files you created/modified, and any issues."

### 3c. Dispatch ALL tasks in the wave simultaneously

Use multiple Agent tool calls in a SINGLE response. This is what enables parallelism.

```
# In one response, dispatch all wave tasks:
Agent(prompt="[t1 prompt]", subagent_type="developer")
Agent(prompt="[t2 prompt]", subagent_type="architect")
```

### 3d. Collect results and token usage

As each agent returns:
- Record: task ID, status (SUCCESS/FAILED), summary of output
- **Extract token usage** from the `<usage>` block returned by the Agent tool. Every agent result includes `total_tokens`, `tool_uses`, and `duration_ms`. Record all three per task.
- If FAILED: mark task and ALL its dependents as BLOCKED

**Token tracking is mandatory.** Accumulate running totals across all tasks for the final report.

### 3e. Handle failures

If a task fails:
```
Task t3 FAILED: [error summary]
Blocked tasks: t4, t5, t6 (all depend on t3 directly or transitively)
Remaining executable: [list any unblocked tasks in later waves]

Options:
  1. Retry t3
  2. Skip t3 and continue with unblocked tasks only
  3. Halt execution entirely

Which option? (ask user)
```

### 3f. Prepare context for next wave

Summarize each completed task's result in 2-3 sentences. This summary is injected into the prompts of dependent tasks in the next wave.

**Do NOT pass raw agent output forward.** Summarize:
- What was produced (files, decisions, artifacts)
- Key constraints for downstream tasks
- Any warnings or caveats

## Step 4: Final Report

After all waves complete (or execution halts):

```
───────────────────────────────────────────
  DAG EXECUTION COMPLETE
───────────────────────────────────────────

  Wave 0  ─── 2 agents ──────────────────
  ⚙️  t1  developer          ✅ Created API schemas
  🏗️  t2  architect          ✅ Created migration

  Wave 1  ────────────────────────────────
  ⚙️  t3  developer          ✅ Implemented handlers

  Wave 2  ─── 2 agents ──────────────────
  🧪  t4  tester             ✅ Wrote integration tests
  🔒  t5  security           ✅ No issues found

  Wave 3  ────────────────────────────────
  🔍  t6  reviewer           ✅ Approved with minor notes

───────────────────────────────────────────
  Tasks:  6/6 completed  |  0 failed
  Waves:  4 executed     |  2 had parallelism
  Saved:  ~33% vs sequential
───────────────────────────────────────────
  💰 Token Economics
───────────────────────────────────────────
  t1  developer        394K tok   $8.28
  t2  architect        322K tok   $6.76
  t3  developer        331K tok   $6.95
  t4  tester           316K tok   $6.64
  t5  security         304K tok   $6.38
  t6  reviewer         326K tok   $6.85
───────────────────────────────────────────
  Total tokens:  1,993K  (1,993,000)
  Est. cost:     $41.86
  Avg per agent: $6.98
  Wall time:     12m 34s (parallel)
  CPU time:      28m 10s (sequential sum)
  Time saved:    55% via parallelism
───────────────────────────────────────────
  📋 Saved to .rune/2026-03-23T14-32-00-api-feature.yaml
───────────────────────────────────────────
```

Use status indicators per task:
- ✅ COMPLETED
- ❌ FAILED
- ⛔ BLOCKED (dependency failed)
- ⏭️ SKIPPED (user chose to skip)
- 🤖 Default emoji if agent not in lookup table

**Mixed-status example** (when some tasks fail):

```
───────────────────────────────────────────
  DAG EXECUTION COMPLETE
───────────────────────────────────────────

  Wave 0  ─── 2 agents ──────────────────
  ⚙️  t1  developer          ✅ Created API schemas
  🏗️  t2  architect          ✅ Created migration

  Wave 1  ────────────────────────────────
  ⚙️  t3  developer          ❌ Build failed: missing dep

  Wave 2  ─── 2 agents ──────────────────
  🧪  t4  tester             ⛔ BLOCKED (t3 failed)
  🔒  t5  security           ⛔ BLOCKED (t3 failed)

  Wave 3  ────────────────────────────────
  🔍  t6  reviewer           ⛔ BLOCKED (t4, t5 blocked)

───────────────────────────────────────────
  Tasks:  2/6 completed  |  1 failed  |  3 blocked
  Waves:  2 of 4 executed
───────────────────────────────────────────
  💰 Token Economics
───────────────────────────────────────────
  t1  developer       ✅  394K tok   $8.28
  t2  architect       ✅  322K tok   $6.76
  t3  developer       ❌        —       —
  t4  tester          ⛔        —       —
  t5  security        ⛔        —       —
  t6  reviewer        ⛔        —       —
───────────────────────────────────────────
  Total tokens:  716K   (completed only)
  Est. cost:     $15.04
  Wall time:     6m 12s
───────────────────────────────────────────
  📋 Saved to .rune/2026-03-23T14-32-00-api-feature.yaml
───────────────────────────────────────────
```

After writing the history file, always show the save confirmation as the last line inside the frame: `📋 Saved to .rune/{filename}`.

Then announce: "DAG execution complete. Using judge-audit to verify."

## Test Mode (Dry Run)

When the user says "test the DAG", "dry run", or "simulate dispatch", run the full validation and wave computation but **do NOT dispatch any agents**. Instead, walk through each wave and simulate results.

### How Test Mode Works

1. **Validate** — run all 6 safety checks (same as live mode)
2. **Compute waves** — display the full pre-dispatch report with emojis (same as live mode)
3. **Simulate each wave** — for each wave, display:

```
═══ Wave 0: SIMULATED ════════════════════
  ⚙️  t1 → developer          Define API schemas
       📂 Files: api/schemas/
       ⏳ Would dispatch to: developer agent
       📤 Expected output: schema files created

  🏗️  t2 → architect          Create database migration
       📂 Files: migrations/
       ⏳ Would dispatch to: architect agent
       📤 Expected output: migration file created
══════════════════════════════════════════
```

4. **Check common DAG problems** — report any of these if found:

| Problem | Check | Display |
|---|---|---|
| **Bottleneck wave** | A wave with only 1 task while others have 2+ | "Wave 1 is a bottleneck (1 task). Can any Wave 2 tasks be moved earlier?" |
| **Over-serialized** | Critical path > 70% of total tasks | "This DAG is heavily serialized (X%). Sequential execution may be simpler." |
| **Underutilized parallelism** | All waves have only 1 task | "No parallelism in this DAG. Execute sequentially instead." |
| **Deep DAG** | More than 6 waves | "Deep DAG (N waves). Context injection may degrade in later waves." |
| **Wide wave** | A wave with 5+ tasks | "Wave N has X tasks. The harness may not dispatch all in one response — consider splitting." |
| **Single-agent DAG** | All tasks assigned to same agent | "All tasks go to the same agent. No multi-agent benefit — execute sequentially." |
| **Disconnected components** | DAG has multiple roots with no shared dependents | "Tasks [A, B] and [C, D] are independent subgraphs. Consider running as two separate DAGs." |

5. **Summary**:

```
───────────────────────────────────────────
  DAG TEST RESULTS
───────────────────────────────────────────
  Validation:     ✅ All 6 checks pass
  Waves:          4 (2 have parallelism)
  Critical path:  67% — DAG dispatch recommended
  Bottlenecks:    None found
  Warnings:       0

  Ready to execute? Use rune
  without "test" to run for real.
───────────────────────────────────────────
```

Test mode is zero-cost — no agents are invoked, no files are modified, no tokens spent on subagents. Use it to verify the DAG structure before committing to execution.

---

## Token Economics

### Data Source

Every Agent tool result includes a `<usage>` block:
```
<usage>total_tokens: 394351 tool_uses: 29 duration_ms: 194810</usage>
```

Extract `total_tokens`, `tool_uses`, and `duration_ms` from every agent result. These are actual metered values, not estimates.

### Cost Estimation

Use this pricing table. Since we only get `total_tokens` (not split input/output), use a blended rate:

| Model | Blended Rate (per 1M tokens) | Notes |
|---|---|---|
| opus | $21.00 | Weighted ~80% input ($15) + ~20% output ($75) |
| sonnet | $4.20 | Weighted ~80% input ($3) + ~20% output ($15) |
| haiku | $1.30 | Weighted ~80% input ($0.80) + ~20% output ($4) |

The 80/20 input/output ratio is a practical approximation for subagent workloads (long context input, moderate output).

**Formula per task:**
```
cost_usd = total_tokens × blended_rate / 1_000_000
```

Use the model from the agent's frontmatter `model:` field. If no model is specified, use the session's default model.

### What to Track Per Task

| Field | Source | Example |
|---|---|---|
| `total_tokens` | `<usage>` block | 394,351 |
| `tool_uses` | `<usage>` block | 29 |
| `duration_ms` | `<usage>` block | 194,810 |
| `model` | Agent frontmatter or session default | opus |
| `est_cost_usd` | Calculated | $8.28 |

### Display Format

**In the final report**, add a `💰 Token Economics` section between the task summary and the save confirmation. See the examples in Step 4 above.

**Formatting rules:**
- Token counts: use `K` suffix (e.g., `394K`) for readability. Round to nearest K.
- Cost: 2 decimal places, USD.
- Wall time: measured from first wave dispatch to last wave completion.
- CPU time: sum of all `duration_ms` across all tasks (the sequential equivalent).
- Time saved: `1 - (wall_time / cpu_time)` as percentage. Only show if >0%.

**For the mixed-status report** (when some tasks fail), show costs only for completed tasks. Failed/blocked tasks show `—` for cost.

### History File Economics

Add an `economics` section to the YAML history file:

```yaml
economics:
  total_tokens: 1020000
  total_cost_usd: 21.42
  model_breakdown:
    opus: { tasks: 3, tokens: 1020000, cost_usd: 21.42 }
  wall_time_ms: 252000
  cpu_time_ms: 574000
  time_saved_pct: 56
  per_task:
    - id: t1
      tokens: 394351
      tool_uses: 29
      duration_ms: 194810
      model: opus
      cost_usd: 8.28
    - id: t2
      tokens: 322517
      tool_uses: 25
      duration_ms: 284405
      model: opus
      cost_usd: 6.76
    - id: t3
      tokens: 304822
      tool_uses: 0
      duration_ms: 98834
      model: opus
      cost_usd: 6.38
```

### Caveat

**These are estimates, not invoices.** The blended rate assumes an 80/20 input/output split. Actual costs depend on the exact input/output token ratio per task, which the Agent tool does not expose. The `total_tokens` value also includes system prompt tokens, tool call overhead, and retry tokens — all of which are billed. Display costs as "Est. cost" (never "Cost") to signal this is approximate.

---

## Proactive Execution Suggestions

**Whenever you produce a plan, remediation list, audit findings, or TODO list with 2+ actionable items, suggest `/rune` execution.** This applies regardless of whether the rune skill was explicitly invoked. Examples:

- After an audit identifies 5 fixes: "Ready to execute these 5 fixes? Run `/rune` to dispatch them in parallel."
- After a planner produces a WBS: "This plan has 14 items across 3 waves. Execute with `/rune`."
- After a judge identifies warnings: "Want to fix these 3 warnings? `/rune` can dispatch the fixes in parallel."
- After exploration identifies tasks: "These 4 tasks are independent — `/rune` can run them simultaneously."

**When NOT to suggest `/rune`:**
- Single-item tasks (just do it directly)
- Pure research with no actionable output
- Tasks that require human judgment before acting

**Phrasing:** Keep it brief. One line at the end of the output:
- "Execute with `/rune`?" (shortest)
- "Ready to dispatch? `/rune`"
- "These N items are parallelizable — `/rune` to execute."

## Dispatch History

Every `/rune` dispatch is persisted to `.rune/` in the project root for audit, recall, and session recovery. This directory is gitignored by default — users who want audit trails can remove the gitignore entry.

### When to write

After Step 4 (Final Report), write a YAML file to `.rune/`. Create the directory if it does not exist.

### File naming

```
.rune/{ISO-timestamp}-{slug}.yaml
```

Example: `.rune/2026-03-23T14-32-00-api-migration.yaml`

The slug is derived from the user's prompt — lowercase, hyphens, max 40 characters. Use the first few meaningful words.

### File format

The history file separates **plan** (intent) from **results** (outcome). This enables replay, audit, and session recovery from the file alone.

```yaml
schema_version: 1
id: "2026-03-23T14-32-00-api-migration"
started: "2026-03-23T14:32:00Z"
completed: "2026-03-23T14:47:12Z"
status: completed               # completed | failed | partial | aborted
trigger: ad-hoc                 # ad-hoc | slash-command | retry | resume
plan_source: ad-hoc             # ad-hoc | write-plan (session) | path/to/PLAN.md
prompt: "implement user service with database migration"

plan:
  - id: t1
    agent: developer
    title: "Define API schemas"
    depends_on: []
    files: [api/schemas/]
    output: "Schema files for user service"
  - id: t2
    agent: architect
    title: "Create database migration"
    depends_on: []
    files: [migrations/]
    output: "SQL migration for user tables"
  - id: t3
    agent: developer
    title: "Implement API handlers"
    depends_on: [t1, t2]
    files: [src/api/]
    output: "Handlers wired to database"

dispatch:
  waves:
    0: [t1, t2]
    1: [t3]
  critical_path: [t1, t3]
  parallelism_benefit: "1.5x"

results:
  - id: t1
    wave: 0
    status: completed
    summary: "Created user.proto with CRUD operations"
  - id: t2
    wave: 0
    status: completed
    summary: "Created 001_create_users.sql migration"
  - id: t3
    wave: 1
    status: completed
    summary: "Implemented handlers with input validation"

economics:
  total_tokens: 1020000
  total_cost_usd: 21.42
  model_breakdown:
    opus: { tasks: 3, tokens: 1020000, cost_usd: 21.42 }
  wall_time_ms: 252000
  cpu_time_ms: 574000
  time_saved_pct: 56
  per_task:
    - id: t1
      tokens: 394351
      tool_uses: 29
      duration_ms: 194810
      model: opus
      cost_usd: 8.28
    - id: t2
      tokens: 322517
      tool_uses: 25
      duration_ms: 284405
      model: opus
      cost_usd: 6.76
    - id: t3
      tokens: 304822
      tool_uses: 0
      duration_ms: 98834
      model: opus
      cost_usd: 6.38

metrics:
  total_tasks: 3
  completed: 3
  failed: 0
  waves_executed: 2
```

### Format notes

- **`plan`** is the full DAG definition — replayable as input to a future dispatch
- **`dispatch`** records computed wave assignments and critical path (planning metadata)
- **`results`** records execution outcomes only — status, summaries, errors
- **`economics`** records token usage, cost estimates, and timing per task
- **`schema_version`** enables future format evolution without breaking old files
- Task `id` is the join key between `plan`, `results`, and `economics.per_task` — the only intentional duplication

### Rules for history files

- **Summaries only in results** — store the 2-3 sentence context summary per task, never raw agent output
- **Create `.rune/` lazily** — only when the first dispatch completes, not at validation time
- **Add `.rune/` to `.gitignore`** if a `.gitignore` exists and `.rune/` is not already listed. Do NOT create a `.gitignore` if one does not exist.
- **Never fail the dispatch** because history could not be written — history is best-effort, not blocking

### Session recovery

If a session is lost mid-dispatch, the user can inspect `.rune/` to see which tasks completed:

1. Read `plan` — full task definitions with file scopes and expected outputs
2. Read `results` — identify tasks with `status: failed` or missing entries (not yet dispatched)
3. Re-dispatch failed/missing tasks using the plan definitions
4. Respect `depends_on` — only re-dispatch if prerequisites are `completed`

To resume: re-run `/rune` with "resume from .rune/{filename}" or re-run with the same prompt — rune reads the history and skips completed tasks.

## Rules

1. **Never skip validation.** Run all 6 safety checks before any dispatch.
2. **Never proceed on ambiguity.** If unsure about a dependency or conflict, ask the user.
3. **Summarize, don't dump.** Context injection between waves is 2-3 sentences per predecessor, not raw output.
4. **File scoping is mandatory.** Every agent prompt includes "Do NOT modify files outside [scope]."
5. **User is the authority.** On any failure or conflict, present options and ask.
6. **Always persist history.** After every dispatch (including failed/partial), write to `.rune/`.
7. **Always track token economics.** Extract usage from every agent result. Display in final report and persist in history.

## Integration

**Produces:** Executed plan with per-task status (persisted to `.rune/`), suitable for `judge-audit` and branch finalization.

**Consumes:** DAG-annotated plan from `write-plan` skill.

**Fallback:** If the plan has no DAG annotations (no `depends_on` fields), tell the user: "This plan is not DAG-annotated. Execute sequentially, or ask the Planner to add dependency annotations."

**Works with:**
- `judge-audit` — after DAG execution completes
- branch finalization — when all tasks complete a feature
- `judge` — code review can be a task in the DAG itself
