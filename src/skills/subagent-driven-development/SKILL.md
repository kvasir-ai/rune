---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session. Dispatches fresh subagent per task with two-stage review (spec compliance then code quality).
---

# Subagent-Driven Development

Execute plan by dispatching fresh subagent per task, with two-stage review after each: spec compliance review first, then code quality review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

## When to Use

- Have an implementation plan with mostly independent tasks
- Want to stay in the current session (no parallel worktrees)
- Want automated review checkpoints between tasks

**vs. executing-plans:** Same session, fresh context per task, two-stage review. Use executing-plans for sequential execution without subagent isolation.

## The Process

1. Read plan, extract all tasks with full text and context
2. For each task:
   a. Dispatch implementer subagent with task text + context
   b. Implementer implements, tests, commits, self-reviews
   c. Dispatch spec reviewer — does code match the spec?
   d. If spec issues: implementer fixes, re-review
   e. Dispatch code quality reviewer — is it well-built?
   f. If quality issues: implementer fixes, re-review
   g. Mark task complete
3. After all tasks: dispatch final reviewer for entire implementation
4. Use finishing-development-branch to complete

## Model Selection

Every subagent dispatch MUST specify an explicit model. Choose based on complexity:

| Role | Complexity | Model |
|---|---|---|
| Implementer | 1-2 files, complete spec | haiku |
| Implementer | 3+ files, cross-module | sonnet |
| Implementer | Architecture decisions, ambiguous spec | opus |
| Spec reviewer | All tasks | sonnet |
| Code quality reviewer | All tasks | sonnet |
| Final reviewer | Entire implementation | opus |

**Escalation:** If haiku returns BLOCKED, re-dispatch with sonnet. If sonnet BLOCKED, re-dispatch with opus. If opus BLOCKED, escalate to the human.

## Handling Implementer Status

- **DONE** — proceed to spec review
- **DONE_WITH_CONCERNS** — read concerns, address if correctness/scope related, then review
- **NEEDS_CONTEXT** — provide missing context, re-dispatch
- **BLOCKED** — assess: more context? more capable model? smaller task? escalate to human?

## Red Flags

**Never:**
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed issues
- Dispatch multiple implementers in parallel (conflicts)
- Start code quality review before spec compliance passes
- Ignore subagent questions

**If reviewer finds issues:**
- Same implementer subagent fixes them
- Reviewer reviews again
- Repeat until approved

## Integration

- **writing-plans** — creates the plan this skill executes
- **requesting-code-review** — code review template for reviewer subagents
- **finishing-development-branch** — complete development after all tasks
- **verification-before-completion** — final evidence check
