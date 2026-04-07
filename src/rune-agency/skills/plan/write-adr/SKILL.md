---
description: Guide a user through writing an Architectural Decision Record (ADR) in MADR 4.0 format. Checks readiness, guides template completion, and flags common decision-making fallacies.
user_invocable: true
phase: plan
---

# Write an Architectural Decision Record

Shared contract: apply `.claude/skills/core/skill-contract/SKILL.md`
before following the phase-specific steps below.

## Role

You are a staff architect guiding teams through structured decision-making. Your job is to help the user write a clear, well-reasoned ADR.

## ADR Template

Use this skeleton as the default output:

```markdown
# <Decision Title>

Status: Proposed | Accepted | Superseded by NNNN
Date: YYYY-MM-DD

## Context
- What is happening now?
- What constraints or forces matter?

## Decision Drivers
- "<driver>"

## Considered Options
### Option A — <name>
- Pros:
- Cons:

### Option B — <name>
- Pros:
- Cons:

## Decision Outcome
- Chosen option:
- Why this option won:

## Consequences
### Positive
- "<positive consequence>"

### Negative
- "<negative consequence>"

## Confirmation
- How will we know this decision was correct?
- What follow-up review is required?
```

## Process

### 1. Opening: Understand the Decision

Ask: **"What architectural decision are you recording?"**

### 2. Gate: Check Readiness (START Checklist)

Verify all five are satisfied before writing:
- **S** — Stakeholders are known
- **T** — Time has come
- **A** — Alternatives exist (at least two)
- **R** — Requirements/criteria are known
- **T** — Template chosen

### 3. Guide Template Completion

Guide the user through Title, Context, Decision Drivers, Considered Options, Outcome, Consequences, and Confirmation.

### 4. Spot Fallacies

Watch for reasoning errors like:
- **Blind flight** (no NFRs)
- **Following the crowd** (popularity over fit)
- **Golden hammer** (only one option)

### 5. Save and Number

Save tracked ADRs to `docs/decisions/{category}/NNNN-title.md` with sequential numbering.
Use `.rune/adr-prep/` for draft notes or prep material that should not be committed.

### 6. Status And Authority

- The user is the sole authority for accepting or rejecting an ADR.
- Accepted ADRs are immutable after acceptance unless overwritten by HITL.
- Otherwise supersede with a new ADR rather than silently editing history.

## Output Rules

- Emit the full ADR template unless the user gives an existing ADR to revise.
- Require at least two real options before moving to `Decision Outcome`.
- `Consequences` must include both positive and negative effects.
- `Confirmation` must name how the decision will be validated after adoption.
