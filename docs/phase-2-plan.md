# Phase 2: Plan

> Decompose work into tasks with explicit dependencies. The dependency graph reveals what can run in parallel.

---

## How Planning Works

The Planner takes the synthesized findings from Phase 1 and produces a structured plan. This is where the DAG comes in.

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

---

## Use rune

Type `/write-plan` to generate a plan from a feature request or design doc. The Planner explores requirements, maps the file structure, decomposes into bite-sized tasks, and annotates with DAG dependencies.

When the plan is ready, type `/rune` to dispatch it.

---

## The DAG Format

A DAG plan has six fields per task. All required.

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

*Previous: [Phase 1: Explore](phase-1-explore.md). Next: [Phase 3: Execute](phase-3-execute.md) — dispatch the plan in parallel waves.*
