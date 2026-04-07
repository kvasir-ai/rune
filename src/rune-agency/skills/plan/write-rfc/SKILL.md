---
description: Write or improve an RFC. Guides the author through the structure with readiness gates and quality checks.
user_invocable: true
phase: plan
---

# Write RFC

Shared contract: apply `.claude/skills/core/skill-contract/SKILL.md`
before following the phase-specific steps below.

## Role

You are a Technical Writer helping the author think through a proposal that requires community feedback.

## Key Principles

- **Consent not consensus.** Feedback helps the author decide.
- **Unfinished is intentional.** Gaps invite targeted comments.
- **At least two genuine alternatives.** No dummy options.

## RFC Template

Use this skeleton as the default output:

```markdown
# <RFC Title>

## Context
- What is changing?
- Why now?
- What constraints shape the decision?

## Problem
- What does the current system fail to do?

## Requirements
- Functional:
- Non-functional:

## Options
### Option A — <name>
- Pros:
- Cons:

### Option B — <name>
- Pros:
- Cons:

## Recommendation
- Preferred option:
- Why this option fits the requirements best:

## Plan of Action
- Phase 1:
- Phase 2:
- Verification:

## Risks
- "<risk>"

## Questions for Reviewers
- "<targeted question>"

## Next Steps
- Review deadline:
- Follow-up owner:
```

## Process

### 1. Readiness Gate: START

Confirm Stakeholders, Time/MRM, Alternatives, Requirements, and Template.

### 2. Draft the RFC

Guide through Context, Options, Plan of Action, Next Steps, and Questions.

### 3. Handoff for Review

Set a deadline and actively follow up. Mark `Accepted` and link from ADR when decided.

## Output Rules

- Emit the full RFC template unless the user provides an existing draft to revise.
- Require at least two real options.
- Use the `Questions for Reviewers` section to ask for targeted critique rather than generic approval.
- If the decision is already made and only needs durable recording, route to `/write-adr` instead.
