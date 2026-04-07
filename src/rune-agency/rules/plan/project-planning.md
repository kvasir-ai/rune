Phase: Plan

# Project Planning Frameworks

> Actionable planning frameworks for structuring implementation work.
> Use when the Planner agent creates implementation plans, breaks down complex features, or assesses plan completeness.

---

## 7 Planning Principles

Use as a checklist when reviewing plan quality. Every plan should demonstrably address the applicable principles.

| # | Principle | Planning Implication | Check |
|---|---|---|---|
| 1 | **Continued justification** | Every plan needs a clear reason to proceed. | Is the business justification still valid? |
| 2 | **Learn from experience** | Capture lessons throughout and apply them. | Are prior learnings reflected? |
| 3 | **Clear roles and responsibilities** | Every task has a named owner. | Are roles and ownership explicit? |
| 4 | **Stage-by-stage delivery** | Plan and control one stage at a time. | Is the plan broken into stages? |
| 5 | **Manage by exception** | Set tolerances for scope, cost, and time. | Are escalation paths clear? |
| 6 | **Focus on outputs** | Define what will be produced before defining how. | Is each task's deliverable defined? |
| 7 | **Tailor to context** | Adapt planning depth to scale and risk. | Is depth proportional to risk? |

---

## Uncertainty Taxonomy

| Type | Definition | Response Strategies |
|---|---|---|
| **Ambiguity** | Unclear requirements, vague scope | Progressive elaboration, prototyping, spikes |
| **Complexity** | Many interconnected parts | Decoupling, iteration, diverse perspectives |
| **Volatility** | Rapid changes in environment | Alternatives analysis, flexible architecture |
| **Risk** | Specific uncertain events | Mitigate, transfer, accept, escalate |

---

## Four-Phase Model Mapping

The Rune Agency lifecycle maps planning themes to four phases.

```
LOAD CONTEXT → EXPLORE → PLAN → BUILD → VALIDATE → SHIP → LEARN
     KM          All     Planner  Agents   Judge      TW      KM
```

### Phase-to-Theme Mapping

| Planning Theme | Four-Phase Stage | Primary Agent | What Happens |
|---|---|---|---|
| **Business Case** | Plan | Planner | Validate justification and value |
| **Organization** | Plan | Planner | Assign agents to tasks |
| **Quality** | Plan / Validate | Planner + Judge | Define acceptance criteria; Judge verifies |
| **Plans** | Plan | Planner | Decompose into DAG tasks |
| **Risk** | Plan / Build | Planner + Judge | Classify risks and validate mitigations |
| **Progress** | Validate / Ship | Judge + Technical Writer | Review state and ship deliverables |

## Plan Completeness Contract

Every substantial plan must make collaboration explicit rather than implied.

| Requirement | What "done" looks like |
|---|---|
| Evidence preservation | research briefs, context packets, or file evidence are referenced directly |
| Ownership | every task or step names a canonical agent owner |
| Artifact routing | tracked outputs go to `docs/plans/` or `docs/decisions/`; ephemeral outputs go to `.rune/` |
| Governance work | taxonomy, docs, profile, or ADR tasks are represented explicitly when affected |
| Validation path | verification commands, validation owner, and human gate are named before Build starts |

## Planning Routing Matrix

| Situation | Required plan shape | Primary collaborator |
|---|---|---|
| parallelizable multi-owner work | DAG | Planner + Judge |
| mostly linear or low-benefit work | Sequential plan | Planner |
| architectural commitment or policy choice | Plan plus ADR task | Technical Writer + HITL |
| terminology, path, or profile drift | Include governance closure task | Knowledge Manager |
| evidence conflict | Return to Explore before decomposition | Researcher or Engineer |

### Core Agent Lifecycle Roles

| Agent | Before | Phase 1: Explore | Phase 2: Plan | Phase 3: Build | Phase 4: Validate | After |
|---|---|---|---|---|---|---|
| **Knowledge Manager** | Load context | Produce context packet and name drift | Flag rule or taxonomy gaps | Recruit supporting agents when needed | Verify doctrine closure | Capture learnings |
| **Planner** | — | Consume research brief plus context packet | Decompose into executable plan | Hand off to `/rune` or user | Accept verdict loopbacks and re-plan | Flag gaps |
| **Judge** | — | Review contradictory evidence on request | Validate plan readiness | — | Review output and route remediation | — |
| **Technical Writer** | — | — | Write ADRs/plans and define artifact shape | Write documentation and surface rendered diffs | Support validation of docs/process changes | Draft PR |

### The Reasoning Pyramid

```
        ┌─────────┐
        │  OPUS   │  Plan + Validate
        │ 3 agents│  Resolve ambiguity, catch what others miss
        ├─────────┤
        │ SONNET  │  Build + Learn
        │ 3 agents│  Write code, implement, structured judgment
        ├─────────┤
        │  HAIKU  │  Explore + Ship
        │ 2 agents│  Read, summarize, follow templates
        └─────────┘
```

**Override guidance:** When dispatching agents as subagents for read-only exploration (Phase 1), override to `haiku` regardless of the agent's default model.

## Exit Criteria For Planning

Planning is complete only when:

- the chosen plan shape is justified as DAG or sequential
- all canonical agent IDs are normalized
- unresolved ambiguity is classified instead of hidden
- verification and validation ownership are named
- the human gate is explicit: `GO`, `WAIT`, or `STOP`

---

## Cross-References

- See `src/rune-agency/rules/plan/architectural-decision-records.md` for architectural decision guidance
- See `src/rune-agency/rules/explore/knowledge-management.md` for knowledge creation cycle
- See `README.md` and `site/index.html` for the current four-phase model overview
