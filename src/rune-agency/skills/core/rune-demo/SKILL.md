---
phase: general
description: Run a showcase DAG example by number (1, 2, or 3). Demonstrates parallel wave dispatch with simulated agents. Use when someone says "run example 1", "dispatch example 2", "show me example 3", or "rune demo".
argument-hint: <1|2|3>
user_invocable: true
---

# rune examples

Shared contract: apply `.claude/skills/core/skill-contract/SKILL.md`
before following the phase-specific steps below.

Run one of three showcase DAGs that demonstrate parallel wave dispatch. Pick the example based on `$ARGUMENTS`.

Use the `rune` skill to execute each example — it handles validation, wave computation, dispatch, final report, and history persistence.

## Example 1: Full-Stack Feature (Fan-Out Diamond)

**When:** `$ARGUMENTS` contains "1" or "feature"

```yaml
tasks:
  - id: t1
    agent: researcher
    title: Research API requirements and existing patterns
    depends_on: []
    files: [docs/api-contract.yaml]
    output: Research brief covering existing endpoints, constraints, and gaps

  - id: t2
    agent: knowledge-manager
    title: Surface terminology and path constraints
    depends_on: []
    files: [src/rune-agency/, docs/]
    output: Context packet covering terminology, rules, and path canon

  - id: t3
    agent: planner
    title: Produce execution-ready implementation plan
    depends_on: [t1, t2]
    files: [docs/plans/]
    output: DAG or sequential plan with verification steps

  - id: t4
    agent: engineer
    title: Implement the feature
    depends_on: [t3]
    files: [src/, tests/]
    output: Working implementation plus verification results

  - id: t5
    agent: technical-writer
    title: Draft supporting docs and PR summary
    depends_on: [t3, t4]
    files: [docs/, CHANGELOG.md]
    output: Updated tracked docs or PR-ready summary

  - id: t6
    agent: judge
    title: Final validation review
    depends_on: [t4, t5]
    files: []
    output: Validation verdict with required owner and next phase
```

**Expected:** 6 tasks, 4 waves, current-canon agent IDs only.

---

## Example 2: Knowledge Refactor (Wide Explore -> Plan -> Validate)

**When:** `$ARGUMENTS` contains "2" or "knowledge"

```yaml
tasks:
  - id: t1
    agent: researcher
    title: Audit outdated references
    depends_on: []
    files: [src/rune-agency/, docs/, site/]
    output: Research brief listing drift and evidence

  - id: t2
    agent: knowledge-manager
    title: Audit taxonomy and profile impact
    depends_on: []
    files: [profiles.yaml, src/rune-agency/]
    output: Context packet with canonical naming changes

  - id: t3
    agent: technical-writer
    title: Rewrite tracked documentation surfaces
    depends_on: [t1, t2]
    files: [docs/user-guide.md]
    output: Updated docs aligned to canonical paths and terminology

  - id: t4
    agent: planner
    title: Create remediation plan
    depends_on: [t1, t2]
    files: [docs/plans/]
    output: Ordered remediation plan with governance tasks

  - id: t5
    agent: judge
    title: Validate knowledge-layer readiness
    depends_on: [t3, t4]
    files: []
    output: Final verdict on whether drift is resolved
```

**Expected:** 5 tasks, 3 waves, parallel Explore fan-out in wave 0.

---

## Example 3: Build Rule Upgrade (Plan -> Build -> Validate)

**When:** `$ARGUMENTS` contains "3" or "rule"

```yaml
tasks:
  - id: t1
    agent: planner
    title: Define the rule-change plan
    depends_on: []
    files: [docs/plans/]
    output: Execution-ready plan with acceptance criteria

  - id: t2
    agent: engineer
    title: Implement rule and validation changes
    depends_on: [t1]
    files: [src/rune-agency/rules/, src/cli/, tests/]
    output: Updated rules, code, and tests

  - id: t3
    agent: technical-writer
    title: Regenerate and inspect docs surfaces
    depends_on: [t1]
    files: [src/cli/site/, site/]
    output: Updated generated docs and review targets

  - id: t4
    agent: judge
    title: Validate the rule-layer upgrade
    depends_on: [t2, t3]
    files: []
    output: Verdict plus loopback owner if blocked
```

**Expected:** 4 tasks, 3 waves, explicit Build -> Validate handoff.

## How to run

Tell the LLM: **"Run rune example 1"** (or 2, 3).

For a dry run (no agents invoked): **"Test rune example 2"**
