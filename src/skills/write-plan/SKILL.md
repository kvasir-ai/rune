---
description: Generate a strict, atomic, step-by-step implementation plan from a design document or feature request. Optimized for automated execution via /rune.
user_invocable: true
---

# Draft Implementation Plan

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for the codebase. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about the toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "Drafting the implementation plan."

**Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## Scope Check

If the spec covers multiple independent subsystems, suggest breaking it into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** If this plan has DAG annotations (depends_on fields), use /rune to dispatch. Otherwise execute sequentially. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## DAG Annotation (for plans with 5+ tasks and 3+ agents)

When a plan has 5 or more tasks involving 3 or more different agents, annotate each task with dependency metadata. This enables parallel dispatch via `/rune`. See `rules/dag-execution-format.md` for the full format specification.

**Add to each task:**
```yaml
- id: t1
  title: "short description"
  agent: agent-name
  depends_on: []          # or [t2, t3] — list of prerequisite task IDs
  output: "what this produces"
  files: ["path/pattern"]  # files this task will touch
```

**After all tasks, add an Execution DAG section:**
```markdown
## Execution DAG

Wave 0 (parallel): t1 (developer), t2 (designer)
Wave 1:            t3 (developer) <- depends on t1, t2
Wave 2 (parallel): t4 (tester), t5 (security) <- depends on t3
Wave 3:            t6 (reviewer) <- depends on t4, t5

Critical path: t1 -> t3 -> t4 -> t6 (4 of 6 tasks, 67%)
Parallelism benefit: 1.5x
Recommendation: DAG dispatch
```

**Rules for DAG annotation:**
- Every task must have a unique `id` (t1, t2, ...)
- `depends_on` must only reference task IDs that exist in the plan
- No circular dependencies
- Two tasks in the same wave must NOT touch the same files
- If unsure about a dependency, ADD it — false dependencies are safe; missing dependencies cause conflicts
- If critical path > 70% of total tasks, note: "Sequential execution recommended"

**Plans with < 5 tasks or only 1-2 agents:** Skip DAG annotation. Use sequential execution.

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.go`
- Modify: `exact/path/to/existing.go:123-145`
- Test: `exact/path/to/file_test.go`

- [ ] **Step 1: Write the failing test**

```go
func TestSpecificBehavior(t *testing.T) {
    result := Function(input)
    if result != expected {
        t.Errorf("got %v, want %v", result, expected)
    }
}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `go test -run TestSpecificBehavior ./path/to/package -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

- [ ] **Step 4: Run test to verify it passes**

- [ ] **Step 5: Commit**
````

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

## Plan Review Loop

After completing each chunk of the plan:

1. Dispatch a plan reviewer subagent with the chunk content and spec document path
2. If issues found: fix and re-dispatch reviewer
3. If approved: proceed to next chunk

**Chunk boundaries:** Use `## Chunk N: <name>` headings. Each chunk should be logically self-contained.

## Execution Handoff

After saving the plan:

**"Plan complete and saved to `docs/plans/<filename>.md`. Ready to execute?"**

- **If plan has DAG annotations:** use `/rune` for parallel wave dispatch
- **If plan has NO DAG annotations:** execute sequentially with checkpoints
