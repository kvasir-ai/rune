Phase: Core

# Agent Collaboration Protocol

> Canonical orchestration source for all agents in the collective.
> Covers routing, escalation, ownership, HITL gates, handoff payloads, and
> decision document triggers.
> See `src/rune-agency/rules/plan/architectural-decision-records.md` for ADR
> format and workflow triggers.

---

## Ownership Matrix

| Concern | Primary owner | Supporting agents | What must survive the handoff |
|---|---|---|---|
| Technical truth | Engineer | Researcher, Judge, Technical Writer | verified behavior, affected paths, exact commands |
| Evidence packet quality | Researcher | Knowledge Manager, Judge | claims, evidence, uncertainty, next owner |
| Execution decomposition | Planner | Researcher, Knowledge Manager, Judge | scope, dependencies, acceptance criteria, risks |
| Rule promotion and taxonomy | Knowledge Manager | Researcher, Technical Writer, Judge | source evidence, affected profiles, naming impact |
| Artifact quality and traceability | Technical Writer | Engineer, Knowledge Manager, Judge | canonical path, audience, links, rendered impact |
| Validation verdicts | Judge | Engineer, Researcher, Technical Writer | findings, evidence, owner, next phase, unblock condition |

Ownership lives here, not in social memory. If two agents disagree and this
table does not resolve it, escalate to HITL.

Hook scripts, hook metadata, companion config, profile wiring, and runtime docs
travel together as one change surface. Do not hand off only the script diff
when runtime automation changed.

## Canonical Agent Identifiers

Use these names in all new plans, rules, and skills.

| Canonical name | Legacy aliases accepted while migrating | Role |
|---|---|---|
| `planner` | — | planning and DAG decomposition |
| `researcher` | — | evidence gathering and uncertainty reduction |
| `knowledge-manager` | `km` | rule promotion, taxonomy, profile hygiene |
| `engineer` | `developer`, `specialist` | implementation and technical verification |
| `technical-writer` | `writer` | durable artifacts and documentation traceability |
| `judge` | `reviewer`, `code-reviewer` | validation verdicts and remediation routing |

Legacy aliases may be translated by workflows during migration. New plans must
emit canonical names.

## Canonical Artifact Interfaces

| Artifact | Producer | Primary consumers | Canonical surface | Required fields |
|---|---|---|---|---|
| Research brief | Researcher | Planner, Judge, Knowledge Manager | inline response or `.rune/research/<slug>.md` | question, findings, evidence, uncertainties, recommended handoff |
| Context packet | Knowledge Manager | Planner, Technical Writer, Judge | inline response or `.rune/context/<slug>.md` | active profile, loaded rules, terminology constraints, known path drift, rule candidates |
| Execution plan | Planner | Engineer, Technical Writer, Judge, user | tracked: `docs/plans/YYYY-MM-DD-<topic>.md`; ephemeral: `.rune/plans/<slug>.md` | scope, success criteria, inputs, assumptions, open questions, tasks, verification, human gate |
| Execution ledger | `/rune` | Judge, user | `.rune/<timestamp>.yaml` | tasks, waves, summaries, statuses, verification |
| Validation verdict | Judge | Planner, Engineer, Technical Writer, user | inline review or `.rune/reviews/<slug>.md` | verdict, findings, evidence, verification run, unverified items, required owner, next phase, unblock condition |
| Rule promotion proposal | Knowledge Manager | user, affected profiles | `src/rune-agency/knowledge/<slug>.md` | source evidence, candidate rule change, affected agents or profiles, terminology impact, validation command, promotion decision |
| ADR | Technical Writer or Planner | user, Engineer, Judge | `docs/decisions/NNNN-<topic>.md` | status, context, options, decision, consequences, confirmation |

Tracked human-review artifacts live in `docs/plans/` and `docs/decisions/`.
Ephemeral workflow artifacts live in `.rune/`. Do not create a parallel
`docs/adrs/` canon.

## Canonical Shared Enums

These values are the authority surface for cross-phase state.

| Field | Allowed values |
|---|---|
| `ambiguity` | `none`, `evidence-gap`, `technical-truth`, `taxonomy`, `business` |
| `blocking_status` | `clear`, `blocked`, `waiting-on-human` |
| `pause_state` | `GO`, `WAIT`, `STOP` |
| `judge_verdict` | `APPROVED`, `APPROVED WITH WARNINGS`, `BLOCKED` |
| `next_phase` | `Explore`, `Plan`, `Build`, `Validate`, `HITL` |

## Handoff Payload Contract

Every agent-to-agent handoff must include all of the following:

- `Goal`: what the receiving agent must decide or produce
- `Input artifact`: files, packets, or prior outputs being consumed
- `Claims or proposed changes`: what is currently believed to be true
- `Evidence`: file paths, commands, URLs, or prior ledgers that support the claim
- `Assumptions`: what has not been proven directly
- `Uncertainties`: what remains open or contradictory
- `Blocking status`: whether work can continue safely
- `Requested next owner`: which agent should act next
- `Re-entry condition`: what must be true before work returns
- `Verification expectation`: what the receiver must check or delegate

If a required field is missing, the receiving agent must stop and route the
work back instead of silently smoothing over the gap.

## Entry Criteria And Return Conditions

| Boundary | Accept when | Return when |
|---|---|---|
| Explore -> Plan | question is bounded, evidence is cited, unknowns are named, recommended next owner is present | evidence is weak, path drift blocks interpretation, or scope is still ambiguous |
| Plan -> Build | tasks have canonical agent IDs, file scope, acceptance criteria, and verification steps | dependencies are unclear, file ownership overlaps, or governance work is missing |
| Plan or Build -> Validate | expected outputs exist, commands run or delegated are recorded, open risks are named, and an owner exists for unresolved items | validation target is unclear, evidence is missing, or the wrong artifact was produced |
| Any phase -> HITL | business choice, unsafe destructive action, conflicting authority surfaces, or unresolved policy contradiction | never bypass HITL when the decision is not purely technical |

## Ambiguity And Escalation Matrix

| Ambiguity class | Route | Expected output |
|---|---|---|
| Missing evidence or contradictory facts | Researcher | research brief with uncertainties |
| Technical truth conflict | Engineer | verified behavior, commands, affected paths |
| Taxonomy, naming, or path drift | Knowledge Manager | context packet and closure recommendation |
| Wrong or weak artifact shape | Technical Writer | corrected artifact or doc-routing recommendation |
| Failed acceptance criteria or cross-phase contradiction | Judge | verdict with next phase and unblock condition |
| Product or business decision | HITL | explicit decision or narrowed scope |

## Sub-Agent Routing

| Type | Definition | Dispatch |
|---|---|---|
| Non-destructive | Read-only: research, analysis, review | Parallelize freely |
| Destructive | Writes files, modifies state | Sequential or single-agent with HITL |

**Parallel** (all required): non-destructive OR independent files, no
inter-task dependencies, clear ownership.

**Sequential** (any trigger): output of A feeds B, shared files or state, scope
unclear.

| Sequential chain | Reason |
|---|---|
| planner -> engineer -> judge | plan -> implement -> validate |
| researcher -> knowledge-manager -> technical-writer | evidence -> doctrine -> durable artifact |

**Consolidation:** dispatch parallel readers -> collect findings -> main agent
synthesizes -> single owner acts. Compact context after consolidation, before
implementation.

**Concurrency cap:** ~10 concurrent subagents; overflow batched. Each returns
`agentId` for resumption.

**Invocation quality:** every dispatch must include specific scope, file
references, context, and success criteria. Handoffs must also satisfy the
payload contract above.

## Human-in-the-Loop Gates

| Checkpoint | Human reviews |
|---|---|
| Plan approval (after execution plan) | approach, scope, affected systems |
| ADR approval | design decisions, migration risks |
| Pre-implementation | code quality, test coverage, PII |
| Pre-PR | change summary |
| Pre-apply (Terraform/K8s) | infra impact, rollback plan |

**Mandatory pauses:** planner (3+ agents -> WAIT) · public API or third-party
adoption -> STOP · unresolved authority conflict -> STOP

Use `GO` when work may continue immediately, `WAIT` when user approval or a
bounded review checkpoint is required, and `STOP` when advancing would be
unsafe or logically invalid.

## Verification Ownership

| Verification question | Primary owner | Supporting owner |
|---|---|---|
| Is the evidence packet sufficient to plan from? | Researcher | Judge |
| Does the plan preserve assumptions, dependencies, and governance work? | Planner | Judge |
| Do technical claims match the repo and runtime? | Engineer | Researcher |
| Does the artifact live in the right place and shape? | Technical Writer | Knowledge Manager |
| Is promotion to rules safe and canonical? | Knowledge Manager | Judge |
| Is the work ready to advance phases? | Judge | HITL |

## Filesystem Memory Locations

| Surface | Purpose |
|---|---|
| `.rune/session-state.json` | runtime workflow state when a workflow is active; schema in `schemas/rune-session-state.schema.json` |
| `.rune/*.yaml` | execution ledgers and wave histories |
| `.rune/research/`, `.rune/context/`, `.rune/reviews/` | optional working artifacts that should not become repo doctrine automatically |
| `src/rune-agency/knowledge/` | durable raw material awaiting Knowledge Manager promotion |

Use `.rune/` for ephemeral workflow memory. Use `src/rune-agency/knowledge/`
only when the finding is stable enough to be considered for reuse.

## Decision Document Triggers

RFC -> ADR -> Design Doc. Small decisions skip RFC.

### RFC Trigger Heuristic

After Explore, suggest `/write-rfc` when two or more hold:
- Multiple viable approaches
- Cross-team or cross-surface impact
- Hard-to-reverse contract or dependency
- Significant cost or timeline impact
- No prior decision recorded

### ADR Trigger Heuristic

Suggest `/write-adr` when any one holds:
- A significant technical choice was just made
- An RFC just closed
- The plan conflicts with or extends an existing ADR
- A verbal or implicit decision is being acted on

Do not suggest ADR for routine configuration changes or implementation details
that do not constrain future choices.

## Subagent Usage

**Use subagent:** verbose output, context isolation, parallel tasks, tool
restrictions, independent verification.

**Use main conversation:** iterative refinement, shared multi-phase context,
quick changes, latency-sensitive.

**Main agent implements. Subagents research and report.** Pattern:
Explore -> Plan -> Build -> Validate.

| Role | Agents |
|---|---|
| Collectors (read + report) | planner, researcher, technical-writer, knowledge-manager |
| Implementers (write code) | engineer |

Implementers lose broader context as subagents - prefer implementation in main
conversation.

**Context protection:** subagents isolate verbose output, return summaries only.
Use filesystem as memory (`.rune/`, `src/rune-agency/knowledge/`). Write raw
data to files, return path. Compact context early. Irrelevant context hurts
more than missing context.

## Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| Silent boundary crossing | Route to owner |
| Escalation skipping | Follow escalation path |
| Heroic single-agent resolution | Collaborate with expert |
| Assuming context in handoffs | Always provide context |
| Dropping evidence during planning | Preserve evidence, assumptions, and uncertainty in the plan |
| Too many subagents | Merge into existing or add to rules/ |
| Subagent for one-line fix | Do it in main conversation |
| 1000+ line agent prompts | Extract shared content to rules/ |

## Cross-References

- See `src/rune-agency/rules/plan/architectural-decision-records.md` for ADR
  format, naming, and directory structure
- See `src/rune-agency/rules/plan/dag-execution-format.md` for execution-plan
  fields and wave semantics
