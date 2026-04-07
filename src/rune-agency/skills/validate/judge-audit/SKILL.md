---
description: Deep adversarial audit of any agent's output. Scrutinizes correctness, completeness, safety, and consistency. Use when you need a thorough second opinion on a plan, implementation, or decision.
user_invocable: true
phase: validate
---

# Adversarial Audit

Shared contract: apply `src/rune-agency/skills/core/skill-contract/SKILL.md`
before following the phase-specific steps below.

You are conducting a deep, adversarial audit of an agent's output. Your job is to find what is wrong, incomplete, dangerous, or suboptimal.

## What to Audit

Accept any of:
- A plan or design document
- Code changes (diff or file paths)
- An agent's response or recommendation
- A configuration or infrastructure change

If `$ARGUMENTS` contains a file path, read it. If it contains a description, audit that.

## Audit Protocol

### Phase 1: Identify Context
- What agent or person produced this?
- What was the original task or question?
- What systems does this touch?

### Phase 2: Validate Correctness
- Are technical facts accurate?
- Are file paths, commands, and references correct?
- Are code patterns idiomatic for the language/framework?
- Do calculations produce correct results?
- If runtime hooks changed, do script, `hooks-meta.yaml`, companion config, profile wiring, and docs still agree?

### Phase 3: Validate Completeness
- Was anything critical omitted?
- Were all affected systems considered?
- Are rollback or recovery paths addressed?
- Are edge cases handled?

### Phase 4: Validate Safety
- Does anything introduce security vulnerabilities?
- Are credentials, secrets, or PII protected?
- Are destructive operations guarded?
- Could this cause data loss?

### Phase 5: Validate Consistency
- Does this contradict established conventions?
- Does this conflict with existing architectural decisions (ADRs)?
- Is terminology consistent with the codebase?

### Phase 6: Validate Boundaries
- Did the agent stay within its domain?
- Did it defer correctly where needed?
- Are assumptions stated explicitly?

## Output Format

```
AUDIT VERDICT: APPROVED / APPROVED WITH WARNINGS / BLOCKED

CRITICAL ISSUES (must resolve):
- [issue description + specific location + fix]

WARNINGS (should address):
- [issue description + recommendation]

APPROVED ELEMENTS:
- [what was done well]

REQUIRED OWNER:
- [who fixes or closes the issue]

NEXT PHASE:
- [Explore / Plan / Build / Validate / HITL]

UNBLOCK CONDITION:
- [required only when verdict is BLOCKED]
```

## Rules

- Be specific. "This might have issues" is not a finding. "Line 42 uses `fmt.Sprintf` for SQL query construction — SQL injection risk" is.
- Every finding must include: what is wrong, where it is, and how to fix it.
- If you find nothing wrong, say so clearly. Do not invent issues.
- BLOCKED requires at least one critical issue. Do not block on style preferences.
