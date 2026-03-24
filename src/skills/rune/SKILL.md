---
name: rune
description: Execute DAG-annotated plans OR ad-hoc parallel dispatches with wave-based visualization. Use when dispatching 2+ agents — whether from a formal plan with depends_on fields, or an improvised research/opinion fan-out. Always shows the dispatch diagram before execution. Computes waves via topological sort, dispatches independent tasks in parallel, collects results, and injects context into dependent tasks.
---

# Executing DAG Plans

## Overview

Execute a DAG-annotated plan by dispatching agents in parallel waves. Each wave contains tasks whose dependencies are all satisfied. Tasks within a wave run simultaneously via multiple Agent calls in a single response.

**Announce at start:** "I'm using the rune skill. Validating DAG before execution."

**Plan source identification:** Determine where the plan came from:
- If executing a plan from a file (e.g., `PLAN.md`, `docs/plans/feature-x.md`), record the file path as the plan source
- If executing a plan produced by the `writing-plans` skill in this session, record `writing-plans (session)`
- If constructing an ad-hoc DAG from a user prompt, record `ad-hoc`

Include the plan source in the dispatch header and history file.

**Prerequisites:**
- Plan must have tasks with `id`, `agent`, `depends_on`, `output`, and `files` fields
- See `rules/dag-execution-format.md` for the canonical format
- For plans WITHOUT DAG annotations, use `executing-plans` instead

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

**If validation fails:**
- Report the SPECIFIC error (which invariant, which tasks, which IDs)
- Do NOT proceed
- Ask the user: "This plan has [error]. Fix and retry, or execute sequentially?"

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

Display a compact dispatch banner with agent emojis:

```
═══ Wave 0: Dispatching 2 agents ═════════
  ⚙️  t1 → developer          Define API schemas
  🏗️  t2 → architect          Create database migration
══════════════════════════════════════════
```

Use the emoji from the lookup table above. If the agent is not in the table, use 🤖.

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

### 3d. Collect results

As each agent returns:
- Record: task ID, status (SUCCESS/FAILED), summary of output
- If FAILED: mark task and ALL its dependents as BLOCKED

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
```

Use status indicators per task:
- ✅ COMPLETED
- ❌ FAILED
- ⛔ BLOCKED (dependency failed)
- ⏭️ SKIPPED (user chose to skip)
- 🤖 Default emoji if agent not in lookup table

Then announce: "DAG execution complete. Using verification-before-completion to verify."

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
| **Underutilized parallelism** | All waves have only 1 task | "No parallelism in this DAG. Use executing-plans instead." |
| **Deep DAG** | More than 6 waves | "Deep DAG (N waves). Context injection may degrade in later waves." |
| **Wide wave** | A wave with 5+ tasks | "Wave N has X tasks. The harness may not dispatch all in one response — consider splitting." |
| **Single-agent DAG** | All tasks assigned to same agent | "All tasks go to the same agent. No multi-agent benefit — use executing-plans." |
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

## Dispatch History

Every dispatch is persisted to `.rune/` in the project root for audit, recall, and session recovery. This directory is gitignored by default — users who want audit trails can remove the gitignore entry.

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
plan_source: ad-hoc             # ad-hoc | writing-plans (session) | path/to/PLAN.md
prompt: "implement gRPC user service with database migration"

plan:
  - id: t1
    agent: developer
    title: "Define API schemas"
    depends_on: []
    files: [api/schemas/]
    output: "Protobuf schema files for user service"
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
    output: "gRPC handlers wired to database"

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
- **`schema_version`** enables future format evolution without breaking old files
- Task `id` is the join key between `plan` and `results` — the only intentional duplication

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

## Rules

1. **Never skip validation.** Run all 6 safety checks before any dispatch.
2. **Never proceed on ambiguity.** If unsure about a dependency or conflict, ask the user.
3. **Summarize, don't dump.** Context injection between waves is 2-3 sentences per predecessor, not raw output.
4. **File scoping is mandatory.** Every agent prompt includes "Do NOT modify files outside [scope]."
5. **User is the authority.** On any failure or conflict, present options and ask.
6. **Always persist history.** After every dispatch (including failed/partial), write to `.rune/`.

## Integration

**Produces:** Executed plan with per-task status (persisted to `.rune/`), suitable for `verification-before-completion`.

**Consumes:** DAG-annotated plan from `writing-plans` skill.

**Fallback:** If the plan has no DAG annotations (no `depends_on` fields), tell the user: "This plan is not DAG-annotated. Use executing-plans for sequential execution, or ask the Planner to add dependency annotations."

**Works with:**
- `verification-before-completion` — after DAG execution completes
- `requesting-code-review` — code review can be a task in the DAG itself
- When all tasks are complete, commit and push work manually or hand off to your human partner for review
