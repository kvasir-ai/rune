---
description: Code review — send completed work for review, or handle incoming review feedback with technical rigor. The default Judge action. Use when completing a task, before merging, or when processing review comments.
user_invocable: true
phase: validate
---

# Code Review

Shared contract: apply `.claude/skills/core/skill-contract/SKILL.md`
before following the phase-specific steps below.

## Sending Work for Review

Dispatch the **Judge** review workflow to catch issues before they cascade. If
the review depends on implementation fixes or technical verification, route the
follow-up to **Engineer**.

**Core principle:** Review early, review often.

### When to Request Review

**Mandatory:**
- After each task in subagent-driven development
- After completing a major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing a complex bug

### How to Request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git merge-base HEAD main)
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch Judge review with:**
- What was implemented
- What it should do (plan or requirements reference)
- Base and head SHAs
- Brief summary

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong (with reasoning)

### Output Contract

Judge review output should preserve:

- verdict
- findings with concrete locations
- required owner
- next phase
- unblock condition when blocked

### Review Template

```markdown
VERDICT: APPROVED | APPROVED WITH WARNINGS | BLOCKED

FINDINGS
- [severity] [file/path:line] <issue and recommendation>

EVIDENCE
- <command, diff, or artifact reviewed>

REQUIRED OWNER
- engineer | planner | technical-writer | knowledge-manager | HITL

NEXT PHASE
- Explore | Plan | Build | Validate | HITL

UNBLOCK CONDITION
- <required when BLOCKED>
```

---

## Handling Review Feedback

Code review requires technical evaluation, not emotional performance.

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

### Forbidden Responses

**NEVER:**
- "You're absolutely right!"
- "Great point!" / "Excellent feedback!" (performative)
- "Let me implement that now" (before verification)

**INSTEAD:**
- Restate the technical requirement
- Ask clarifying questions
- Push back with technical reasoning if wrong
- Just start working (actions > words)

### The Response Pattern

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

### Feedback Response Template

```markdown
Issue: <restated technical requirement>
Assessment: <agree / disagree / partially agree, with reasoning>
Action: <fix made or clarification requested>
Verification: <test, diff, or command>
```

### When to Push Back

Push back when:

- the suggestion breaks existing functionality
- the reviewer lacks critical context
- the change would add speculative scope
- the recommendation is technically incorrect for this codebase
- the recommendation conflicts with current architectural decisions
