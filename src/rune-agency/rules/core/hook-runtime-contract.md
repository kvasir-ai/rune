Phase: Core

# Hook Runtime Contract

> Canonical doctrine for Rune runtime hooks, hook metadata, companion config,
> and workflow-state integration.
> Use this rule whenever a task creates, edits, validates, or documents hooks.

---

## Canonical Hook Bundle

Every hook is a bundle, not a lone script. Treat all of these as one contract:

| Surface | Canonical location | Purpose |
|---|---|---|
| Hook script | `src/rune-agency/hooks/<phase>/<name>.py` | executable runtime behavior |
| Hook bindings | `src/rune-agency/hooks-meta.yaml` | event, matcher, timeout wiring |
| Companion config | same phase directory as the hook script | runtime data such as safety patterns or formatter rules |
| Profile wiring | `profiles.yaml` | opt-in deployment surface |
| Runtime state | `.rune/session-state.json` when workflow-aware | shared workflow context for Notification / Stop hooks |
| User-facing docs | `AGENTS.md`, `src/cli/site/sections/hooks/`, generated `site/` | human explanation of runtime behavior |

If one of these changes, check whether the others must change too.

## Phase Ownership

| Hook phase | Typical responsibility |
|---|---|
| `core` | cross-cutting safety, session discipline, workflow awareness |
| `explore` | research or discovery nudges |
| `plan` | planning discipline and decomposition safeguards |
| `build` | write-time automation and execution-time quality checks |
| `validate` | done gates, stop checks, verdict reinforcement |

Do not use flat source paths such as `src/rune-agency/hooks/safety-check.py` as
canon. Source hooks are phase-scoped.

## Event Contract

| Event | Hook behavior requirement |
|---|---|
| `PreToolUse` | deterministic, fast, side-effect minimal; may deny execution |
| `PostToolUse` | may modify the touched artifact or emit warnings; must resolve files relative to the active project root |
| `Notification` | return compact JSON with `decision: continue` and short `additionalContext` only when useful |
| `Stop` / `SubagentStop` | emit concise completion guidance and tolerate missing workflow state without crashing |

Hook outputs should be minimal. Hooks are runtime guardrails, not a second
conversation.

## Companion Config Doctrine

- Keep hook companion files beside the owning hook in the same phase directory.
- If a hook depends on companion config, validation must fail when the companion
  file is missing.
- If a hook can safely degrade without a tool or local dependency, degrade
  predictably and document the behavior.
- Prefer explicit config over hard-coded rule lists in Python when the behavior
  is meant to be user-editable.

## Change Protocol

When hook behavior changes, check all of the following:

- script logic
- `hooks-meta.yaml`
- companion config files
- `profiles.yaml`
- targeted tests
- rules / skills / agents that teach the affected workflow
- generated docs or onboarding surfaces

Hook changes are cross-surface changes by default. Do not ship them as isolated
script edits unless you have proved that no other surface changed.

## Collaboration Expectations

| Change type | Primary owner | Supporting owner |
|---|---|---|
| Runtime semantics or script logic | Engineer | Judge |
| Profile or taxonomy drift | Knowledge Manager | Technical Writer |
| User-facing docs and examples | Technical Writer | Knowledge Manager |
| Evidence gathering for observed runtime behavior | Researcher | Engineer |
| Final safety / correctness gate | Judge | HITL |

Planner should schedule explicit hook-governance work whenever a task changes
hook names, events, companion config, workflow-state fields, or deployment
paths.

## Minimum Verification

When hook surfaces change, run all applicable checks:

- `rune system validate`
- `tests/test_rune.py`
- any hook-specific or site-generation tests that cover the changed surface
- `bash .github/workflows/scripts/build-site.sh` if rendered docs changed

If the hook change affects deployed behavior, surface the rendered docs or
workflow review target for HITL.

## Cross-References

- See `src/rune-agency/rules/core/agent-collaboration.md` for ownership and
  handoff rules
- See `src/rune-agency/rules/core/rune-operations.md` for repository layout and
  deployment workflow
- See `src/rune-agency/rules/build/execution-contract.md` for runtime build
  behavior when hooks are active
