# The Three-Phase Model

> How knowledgeable agents collaborate: explore, plan, execute. The core idea behind rune.

---

## The Core Idea

A single generalist agent doing everything is like a single developer who is simultaneously a database engineer, security auditor, frontend developer, and infrastructure architect. They can do each job, but not as well as a specialist — and certainly not in parallel.

**Knowledgeable agents** are specialists. Each one carries domain-specific rules, patterns, and conventions in its context window. A developer agent knows your coding conventions, module structure, and testing patterns. A security agent knows compliance requirements and threat modeling. They don't need to learn — they arrive with expertise loaded.

What makes agents "knowledgeable" is not conversation history — it is **pre-loaded rule files**. Each agent starts with domain-specific conventions, patterns, and checklists already in its context window before the first prompt arrives. This is what separates a named agent from "the same LLM with a different label" — the label alone does nothing; the rules do everything.

The insight is that most engineering work decomposes into tasks that different specialists can execute simultaneously, with a thin coordination layer between them.

---

## The Three Phases

Every non-trivial task follows the same lifecycle:

```
Phase 1: EXPLORE    →    Phase 2: PLAN    →    Phase 3: EXECUTE
(understand)              (decompose)            (build + verify)
```

### Phase 1: Explore

Before doing anything, understand the problem. Dispatch read-only agents in parallel to gather context from different angles. They research, analyze, and return summaries — they never write code.

```
════════════════════════════════════════════════
  FAN-OUT EXECUTION
  Agents: 4  |  Waves: 2  |  Type: research
════════════════════════════════════════════════

  Wave 0 ──── parallel ───────────────────────
  #1  DEVELOPER             Read existing API structure
  #2  RESEARCHER            Check upstream data sources
  #3  SECURITY              Assess compliance requirements
  #4  TESTER                Review current test coverage

  Wave 1 ──── sequential ─────────────────────
  #5  JUDGE                 Synthesize all findings
                             → #1, #2, #3, #4

════════════════════════════════════════════════
```

**Why this works:** Four agents reading four different parts of the codebase simultaneously. Each returns a 2-3 sentence summary. The Judge merges them into a unified picture. Total wall time: ~2 minutes. Sequential equivalent: ~8 minutes.

**Key principle:** Subagents are context collectors, not implementers. They read and report. The main conversation (or a Planner) takes their findings and builds the plan.

### Phase 2: Plan

The Planner takes the synthesized findings and produces a structured plan. This is where the DAG comes in.

A good plan identifies:
- **What** needs to happen (tasks)
- **Who** does each task (agent assignment)
- **What depends on what** (the dependency graph)
- **What can run in parallel** (independent tasks in the same wave)

```yaml
tasks:
  - id: "#1"
    agent: developer
    title: "Add new API endpoint"
    depends_on: []
    files: [internal/handler/]

  - id: "#2"
    agent: developer
    title: "Add calculation layer"
    depends_on: []
    files: [src/calc/]

  - id: "#3"
    agent: developer
    title: "Wire endpoint to backend"
    depends_on: ["#1", "#2"]
    files: [internal/engine/]

  - id: "#4"
    agent: reviewer
    title: "Review all changes"
    depends_on: ["#1", "#2", "#3"]
    files: []
```

**The DAG reveals the parallelism:**

```
Wave 0:  #1 DEVELOPER,  #2 DEVELOPER
Wave 1:  #3 DEVELOPER           ← waits for #1, #2
Wave 2:  #4 REVIEWER            ← waits for all

Critical path: #1 → #3 → #4  (3 of 4 tasks = 75%)
Benefit: 4/3 = 1.33x faster than sequential
```

Tasks #1 and #2 have no dependencies on each other — different agents working on different files. They run simultaneously. Task #3 needs both to exist first. Task #4 reviews everything at the end.

### Phase 3: Execute

The DAG dispatcher takes the plan and executes it wave by wave:

1. **Wave 0**: Dispatch #1, #2 in parallel (multiple Agent calls in one response)
2. **Collect results**: Each agent returns a summary of what it built
3. **Inject context**: Summarize Wave 0 results into Wave 1 prompts (2-3 sentences per predecessor — never dump raw output)
4. **Wave 1**: Dispatch #3 with context from #1 and #2
5. **Wave 2**: Dispatch #4 (code review) with context from all prior tasks
6. **Report**: Show token usage, cost, and time saved

**Inter-wave context injection — what it actually looks like:**

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

### Error Handling

If a task fails, all dependent tasks are automatically blocked. The dispatcher reports the failure and presents three options: retry the failed task, skip it and continue with unblocked tasks, or halt entirely. The human decides — agents never silently swallow failures.

---

## Collaboration Patterns

### Pattern 1: Feature Implementation

The most common workflow. A human requests a feature; agents plan, build, and verify.

```
Human: "Add a retirement projection layer"

  ┌─────────────────────────────────────────┐
  │  PLANNER reads the request, explores    │
  │  the codebase, writes a plan            │
  └──────────────┬──────────────────────────┘
                 │
         [Human approves plan]
                 │
  ┌──────────────┴──────────────────────────┐
  │  Wave 0 ──── parallel                   │
  │  DEVELOPER         Add calc layer       │
  │  DEVELOPER         Add API endpoint     │
  │  TESTER            Write test fixtures  │
  └──────────────┬──────────────────────────┘
                 │
  ┌──────────────┴──────────────────────────┐
  │  Wave 1 ──── sequential                 │
  │  DEVELOPER         Wire API to backend  │
  └──────────────┬──────────────────────────┘
                 │
  ┌──────────────┴──────────────────────────┐
  │  Wave 2 ──── parallel                   │
  │  REVIEWER          Review code quality  │
  │  SECURITY          Review compliance    │
  └──────────────┬──────────────────────────┘
                 │
         [Human approves PR]
```

### Pattern 2: Incident Investigation (Fan-Out + Converge)

Something is broken. Multiple specialists investigate simultaneously, then a Judge synthesizes.

```
  Wave 0 ──── parallel (fan-out) ─────────────
  #1  DEVELOPER          Check application logs
  #2  TESTER             Check test failures
  #3  SECURITY           Check for auth failures

  Wave 1 ──── sequential ─────────────────────
  #4  JUDGE              Root cause analysis
                          → #1, #2, #3
```

Four specialists looking at four different angles simultaneously find the root cause in the time it takes one generalist to check the first angle.

### Pattern 3: Sequential Chain

Some workflows are inherently sequential — each step depends on the previous one.

```
  DEVELOPER  → Creates the schema
  DEVELOPER  → Implements the handler (needs schema)
  TESTER     → Writes tests (needs handler)

  [Human verifies]
```

**No DAG parallelism here** — and that's fine. The DAG format handles both. Tasks with `depends_on: []` run in parallel; tasks with dependencies wait. The dispatcher automatically does the right thing.

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

## Context Management: The Hidden Efficiency

The biggest cost in LLM-based systems is not compute — it is context. Every file read, every log line, every query result that enters a context window displaces space for reasoning.

Subagents solve this by making context **ephemeral**. Each subagent starts with a fresh context window. It reads as much as it needs, does its analysis internally, and returns only a distilled summary. When the subagent completes, its heavy context dies. Only the summary survives in the parent.

**The core insight: the main context window never sees the raw material. It sees only the finished product.**

```
Subagent internally: 300K tokens (file reads, log parsing, query results, dead ends)
  → Returns to parent: "The staging model has a NULL handling bug in the price
     column. Line 47 passes through NULLs that should be filtered."

Parent receives: 42 tokens. Not 300K.
```

| Subagents Dispatched | Total Work Done | Main Context Growth | Budget Used |
|---|---|---|---|
| 1 | ~130K tokens | ~100 tokens | Negligible |
| 5 | ~650K tokens | ~500 tokens | Under 0.1% of 1M window |
| 10 | ~1.3M tokens | ~1,000 tokens | 0.1% |
| 20 | ~2.6M tokens | ~2,000 tokens | 0.2% |

This is what makes deep DAGs practical. A 12-wave, 20-task DAG can dispatch agents that collectively process millions of tokens. The main context holds only the accumulated summaries and stays fast, focused, and accurate from the first wave to the last.

---

## Why Planning + DAG = Better Economics

| Approach | Problem |
|---|---|
| **One agent does everything** | Massive context window, loses focus, mistakes in unfamiliar domains |
| **Agents dispatched ad-hoc** | No coordination, duplicated work, file conflicts |
| **Plan first, then dispatch** | Each agent gets a focused prompt. No wasted tokens. No rework. |

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

## The DAG Format

A DAG plan has five fields per task. All required.

```yaml
tasks:
  - id: t1
    agent: architect
    title: Design API contract
    depends_on: []
    files: [docs/api-contract.yaml]
    output: API schema with endpoints and error codes

  - id: t2
    agent: developer
    title: Implement API handlers
    depends_on: [t1]
    files: [src/api/]
    output: Working handlers wired to database
```

| Field | What It Does |
|---|---|
| `id` | Unique identifier — the task's name in the dependency graph |
| `agent` | Who does the work — must match an agent in your team |
| `title` | What gets done — imperative verb phrase |
| `depends_on` | What must finish first — empty list means no prerequisites |
| `files` | What this task touches — used to detect conflicts between parallel tasks |
| `output` | What this task produces — tells dependent tasks what to expect |

The key decision is `depends_on`. Ask: "Can this task start before that task finishes?" If yes, do not add the dependency. If no, add it. When unsure, add it — a false dependency costs parallelism; a missing dependency causes a race condition.

### Two Ways to Get a DAG

**Path A: Ask the Planner.** Describe what you want in plain English. The Planner breaks it into tasks with dependencies. You type `/rune`. No YAML required.

**Path B: Write it yourself.** Paste the YAML directly and type `/rune`. The dispatcher validates and executes.

### Validation

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

### Ad-Hoc Dispatch

You do not always need a formal plan. Sometimes you want three opinions on the same question.

```
You: "I need perspectives on whether to use WebSockets or SSE. /rune"
```

rune constructs a DAG on the fly — three independent assessments feeding into one Judge synthesis. No YAML. No plan file. The dispatcher identifies that parallel work feeds into a convergence step, builds the implicit DAG, and dispatches it.

### When NOT to Use DAG Dispatch

| Situation | Do This Instead |
|---|---|
| Fewer than 4 tasks | Run sequentially |
| All tasks go to the same agent | Run sequentially |
| Linear chain with no branching | Run sequentially |
| Critical path exceeds 70% of total tasks | Run sequentially |

The threshold is a 1.3x speedup. Below that, sequential execution is simpler and nearly as fast. Test before committing: say "test this DAG" for a zero-cost dry run.

---

## History and Recovery

Every `/rune` dispatch is saved to `.rune/` in the project root. Each file contains the full plan, wave assignments, per-task results, and token economics.

If a session dies mid-dispatch, the history file shows which tasks completed. Resume by running `/rune` with "resume from .rune/{filename}" — rune reads the file, skips completed tasks, and picks up where it left off.

The `.rune/` directory is gitignored by default. If you want audit trails in version control, remove the gitignore entry.

---

*The shortest path from ignorance to answer is the one where nothing waits unnecessarily.*
