---
description: Shared doctrine for Rune Agency skills. Defines canonical agent IDs, tracked vs ephemeral artifact paths, pause states, current command family, and handoff expectations.
phase: general
user_invocable: false
---

# Skill Contract

This is the shared contract for Rune Agency skills. Phase-specific skills should
follow this doctrine instead of inventing their own taxonomy or artifact canon.

## Canonical Agent IDs

Use these names in new skill examples, plans, and handoffs:

- `planner`
- `researcher`
- `knowledge-manager`
- `engineer`
- `technical-writer`
- `judge`

## Canonical Artifact Paths

| Surface | Use |
|---|---|
| `docs/plans/` | tracked human-review plans |
| `docs/decisions/` | tracked ADRs |
| `.rune/` | ephemeral ledgers, briefs, draft packets, and local workflow state |
| `src/rune-agency/knowledge/` | durable raw material awaiting promotion |

Do not teach `docs/adrs/` as a tracked path.

## Canonical Hook Surfaces

When a skill talks about runtime automation, use the real hook bundle:

- `src/rune-agency/hooks/<phase>/<name>.py`
- `src/rune-agency/hooks-meta.yaml`
- hook companion config beside the owning script
- `profiles.yaml` for hook enablement
- `.rune/session-state.json` for workflow-aware hooks

Do not teach flat source paths or pretend the script alone is the full change.

## Canonical Pause States

Use:

- `GO` when work may continue immediately
- `WAIT` when bounded review or approval is required
- `STOP` when advancing would be unsafe or logically invalid

## Command Family

Use the `rune` command family in examples and instructions:

- `rune profile use ...`
- `rune system validate`
- `rune system verify`

Do not teach `make ...` commands as the primary canon.

## Skill Output Expectations

Every substantial skill should define:

- required inputs
- artifact or response output
- stop conditions
- validation or handoff expectations

If the skill changes hooks, also name the affected metadata, profile, and docs
surfaces.

If a skill routes work into another phase, name the next owner and the artifact
being handed off.

## External Fetch Policy

Use local repo truth first. Reach for web or remote catalog sources only when
the local repo cannot answer the question or the task explicitly requires an
external source.
