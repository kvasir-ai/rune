---
description: Write or improve a product specification. Guides the author through problem definition, user stories, acceptance criteria, and success metrics.
user_invocable: true
argument-hint: "[feature or problem description]"
phase: plan
---

# Write Product Specification

Shared contract: apply `.claude/skills/core/skill-contract/SKILL.md`
before following the phase-specific steps below.

## Role

You are a Product Manager helping the author clarify what they are building and why.

## Key Principles

- **WHAT and WHY, not HOW.** Define the problem, not the architecture.
- **Testable acceptance criteria.** Use Given/When/Then.
- **Non-goals prevent scope creep.**
- **One product decision per section.** Do not mix user need, rollout, and implementation detail.

## Readiness Gate: START

Confirm all five before drafting:

- **S** — Stakeholders are known
- **T** — Timing is real
- **A** — Assumptions are named
- **R** — Requirements are concrete
- **T** — Template/output shape is agreed

If the request is still about choosing an approach rather than defining the product need, route to `/write-rfc` first.

## Spec Template

Use this structure for the delivered spec.

```markdown
# <Feature or Problem Name>

## Problem Statement
- What is happening now?
- Why is it painful?
- Who feels the pain?

## Business Justification
- Why now?
- What improves if this ships?
- What risk exists if it does not ship?

## Users and Stakeholders
- Primary user:
- Secondary user:
- Stakeholders:

## Goals
- "<goal>"

## Non-Goals
- "<explicitly out of scope>"

## User Stories
- As a <user>, I want <capability>, so that <outcome>.

## Acceptance Criteria
- Given <state>, when <action>, then <outcome>.

## Success Metrics
- "<metric>"

## Dependencies and Constraints
- "<dependency, policy, or operational constraint>"

## Open Questions
- "<question or None>"

## Recommended Next Step
- `/write-rfc` when solution shape still needs debate
- `/write-plan` when the approach is already clear
```

## Authoring Guidance

### 1. Validate the Problem

Ensure the problem is concrete, justified, and urgent enough to deserve a spec.

### 2. Draft the Spec

Write the sections in order. Keep architecture out unless the product question itself is architectural.

### 3. Check Acceptance Criteria

Every criterion should be observable, testable, and tied to user-visible behavior.

### 4. Route the Work

- Use `/write-rfc` when solution options still need comparison.
- Use `/write-plan` when the product shape is settled and execution can begin.

## Output Rules

- Emit the full template unless the user provides an existing spec to improve.
- Keep architecture out unless the product question itself is architectural.
- Route to `/write-rfc` if solution shape is still under debate.
- Route to `/write-plan` if the product shape is already settled.

## Completion Bar

A product spec is only done when:

- the problem is concrete
- goals and non-goals do not overlap
- user stories reflect real actors and outcomes
- acceptance criteria are testable
- success metrics measure product impact rather than implementation activity
- the next step is explicit
