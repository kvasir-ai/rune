Phase: Validate

# Collaboration Validation Contract

> Validation doctrine for cross-phase handoffs, verdict shape, and remediation
> routing.

---

## Required Validation Manifest

Every substantial validation pass should consume or reconstruct a manifest with:

- `target`: the artifact, plan, implementation, or doc being reviewed
- `acceptance_criteria`: what the work must satisfy
- `evidence`: files, briefs, ledgers, or commands that support the review
- `verification_run`: what was actually executed or delegated
- `unverified_items`: what remains uncertain
- `open_risks`: non-blocking concerns that still matter
- `proposed_next_phase`: where the work should go if approved
- `required_owner`: who must act if the verdict is not approved
- `unblock_condition`: what must become true before re-validation

If the manifest cannot be assembled, return the work to the previous owner
instead of guessing.

## Verdict-State Mapping

| Judge verdict | Runtime meaning | Required follow-up |
|---|---|---|
| `APPROVED` | ready to advance | record evidence and move to next phase |
| `APPROVED WITH WARNINGS` | advance allowed, risk remains | record warnings, owner, and review expectation |
| `BLOCKED` | do not advance | name failed contract, owner, return phase, and unblock condition |

Use the canonical enums from
`.claude/rules/core/agent-collaboration.md`.

## Loopback Matrix

| Failure mode | Return phase | Primary owner |
|---|---|---|
| Evidence gap or contradictory facts | Explore | Researcher |
| Missing scope, task structure, or acceptance criteria | Plan | Planner |
| Incorrect implementation or failed technical verification | Build | Engineer |
| Wrong artifact type, stale path, or broken wording surface | Plan | Technical Writer |
| Taxonomy, terminology, or profile drift | Explore | Knowledge Manager |
| Business or policy conflict | HITL | user |

## Validation Ownership

| Question | Primary owner | Supporting owner |
|---|---|---|
| Are claims backed by evidence? | Judge | Researcher |
| Does implementation match the repo and runtime? | Engineer | Judge |
| Is the artifact canonical and traceable? | Technical Writer | Knowledge Manager |
| Can doctrine be promoted safely? | Knowledge Manager | Judge |

## Build -> Validate Handoff Minimum

Build work is not ready for validation until all of the following exist:

- the execution ledger records task statuses and summaries
- commands actually run are captured or explicitly marked delegated
- unresolved risks are named with an owner
- the produced artifact matches the expected path and type
- any `WAIT` or `STOP` conditions from Build are resolved or carried forward

If the target changed hooks or runtime guardrails, validation also requires:

- the hook script, metadata, and companion config paths
- evidence that profile wiring still references the correct hook names
- evidence that runtime docs or onboarding surfaces were updated when behavior changed

## Cross-References

- See `.claude/rules/core/agent-collaboration.md` for the shared
  handoff contract
- See `.claude/agents/validate/judge.md` for verdict requirements
