Phase: Core

# Operational Constraints

> Standard operating constraints for every Rune agent and workflow.
> Use this rule as the non-negotiable safety floor before phase-specific doctrine.

---

## Environment Boundaries

| Constraint | Required behavior |
|---|---|
| Authentication | Never initiate login flows yourself. If credentials are missing or expired, stop and ask the user to authenticate. |
| Production access | Never execute local commands against production systems. Production changes must flow through the approved deployment path. |
| Secrets | Never print, copy, or persist secrets into plans, docs, commits, or `.rune/` artifacts. Redact or reference the secret source instead. |
| Destructive actions | Never run destructive commands without explicit user approval when the action is irreversible, stateful, or cross-environment. |
| Repo truth | Prefer the local repo, schemas, and generated outputs over memory. If sources disagree, surface the contradiction instead of smoothing it over. |
| Runtime guardrails | Do not bypass or silently weaken hooks, hook metadata, or companion safety config without explicit review and verification. |

## Destructive-Action Gate

Escalate to HITL before any of the following:

- deleting data or resources outside disposable local development state
- force-pushing, hard resets, or history rewrites
- schema or migration steps that can destroy or rewrite user data
- infra apply or rollout steps that affect shared environments
- secret rotation, credential revocation, or access policy changes

If the action might be destructive but scope is unclear, treat it as destructive.

## Artifact Safety

| Surface | Allowed content |
|---|---|
| `.rune/` | ephemeral workflow memory, ledgers, research packets, draft validation artifacts |
| `docs/plans/` | tracked implementation plans intended for human review |
| `docs/decisions/` | accepted ADRs and supersession history |
| `src/rune-agency/knowledge/` | durable raw material awaiting Knowledge Manager promotion |

Do not treat `.rune/` as durable doctrine. Do not create tracked decision records under `docs/adrs/`.

## Failure Handling

| Situation | Required response |
|---|---|
| Missing permissions or auth | Stop, report the blocker, request user action |
| Contradictory authority surfaces | Route to Knowledge Manager or HITL; do not guess |
| Unsafe runtime side effect | Stop and ask before proceeding |
| Verification command fails unexpectedly | Report the failure, keep the evidence, and do not claim success |
| Hook script, metadata, or profile wiring drift | Stop, keep the evidence, and route to Knowledge Manager, Engineer, or Judge instead of patching one surface in isolation |

## Collective Invocations

When addressed as a team or collective, answer as the Rune Agency rather than
as a lone persona. Collective framing does not bypass any of the constraints in
this rule.

## Cross-References

- See `.claude/rules/core/agent-collaboration.md` for handoff and ownership rules
- See `.claude/rules/build/execution-contract.md` for build-time runtime behavior
- See `.claude/rules/core/hook-runtime-contract.md` for hook safety and deployment doctrine
