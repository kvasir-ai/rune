# The Context Budget

> Why context management matters, how rune keeps it lean, and how to measure your footprint.

---

## The Problem

Every token loaded into an LLM's context window displaces space for reasoning. Load too much and the model has less room to think. Load too little and it lacks the knowledge to act well.

Most AI agent frameworks ignore this trade-off. They load everything they have — every agent definition, every tool description, every rule — and hope the model figures out what matters. On a 200K context window, a framework that consumes 80K tokens at startup leaves 120K for actual work. That is 60% of your budget spent before the first prompt.

rune treats context as a budget. Every token loaded must earn its place.

---

## What Loads When

Not everything loads at once. rune has three loading tiers:

| Tier              | What                                               | When                            | Cost              |
| ----------------- | -------------------------------------------------- | ------------------------------- | ----------------- |
| **Session start** | Agent frontmatter (descriptions, not full prompts) | Always                          | ~3K tokens        |
| **Session start** | Rules deployed by the active profile               | Always                          | Varies by profile |
| **Session start** | Hooks (safety-check, auto-lint)                    | Always                          | ~3K tokens        |
| **On demand**     | Skill full text                                    | When a slash command is invoked | ~1-2K per skill   |
| **On demand**     | Agent full prompt                                  | When a sub-agent is dispatched  | ~1-5K per agent   |

The distinction matters. A skill that is never invoked costs zero tokens. An agent that is never dispatched loads only its frontmatter description (~150 tokens), not its full system prompt.

This is why the at-rest footprint is much smaller than the total content in `src/`.

---

## Profiles Are the Lever

A profile controls which rules load at session start. All agents and skills deploy to every profile — but rules are profile-specific.

A platform engineer working on Terraform does not need financial planning rules. A financial analyst does not need Kubernetes conventions. Profiles enforce this separation:

```bash
make use-profile PROFILE=my-infra-profile     # loads infra rules only
make use-profile PROFILE=my-finance-profile   # loads finance rules only
```

Each profile has a different context footprint. The default profile ships lean — collaboration rules and project management. Add domain-specific rules as you need them, and measure the impact.

---

## Measuring Your Footprint

```bash
make context-budget
```

This shows what the active profile costs:

```
==> Context budget for profile: default

  Agents (frontmatter):       ~3195 tokens  [session start]
  Rules (7 deployed):         ~16082 tokens  [session start]
  Hooks:                      ~2746 tokens  [session start]
  Skills:                     ~21550 tokens  [on demand]

  At rest (no skills):        ~22023 tokens
  Context usage (200K):       ~11%
```

**At rest** is the number that matters — it is what loads before you type anything. Skills are excluded because they load only when invoked.

---

## Budget Guidelines

| Context Window | At-Rest Budget | Remaining for Work | Guidance                                                                    |
| -------------- | -------------- | ------------------ | --------------------------------------------------------------------------- |
| 200K tokens    | ~22K (11%)     | ~178K              | Default profile. Room for long sessions, large files, multi-step reasoning. |
| 200K tokens    | ~50K (25%)     | ~150K              | Heavy profile with domain rules. Still comfortable for most work.           |
| 200K tokens    | ~80K (40%)     | ~120K              | Approaching the limit. Consider splitting into two profiles.                |
| 1M tokens      | ~22K (2%)      | ~978K              | Context is effectively unlimited. Load what you need.                       |

The 200K window is the constraint that matters. On 1M context, even a heavy profile barely registers. But most users are on 200K — design for the constraint, not the exception.

---

## How to Keep It Lean

**Split large rules.** A rule over 500 lines is a candidate for splitting into focused sub-rules deployed to different profiles. The Knowledge Manager agent can identify these during audits.

**Profile per role.** Do not load infrastructure rules when doing financial analysis. Create profiles that match your workstreams.

**Archive stale rules.** Rules that have not been updated in six months and contain version-specific content are candidates for archival. Archived rules move to `src/knowledge/` — they stop consuming context but remain available for reference.

**Measure after changes.** Run `make context-budget` after adding or removing rules. A rule that looks small in isolation can push a profile past the comfortable threshold when combined with others.

---

## Why Sub-Agents Help

When rune dispatches a sub-agent via `/rune`, the sub-agent gets its own context window. Research, exploration, and verbose tool output stay in the sub-agent's context — only a summary returns to the main session.

This is context quarantine. The main session stays lean even during complex multi-agent work. Each wave of a DAG dispatch produces summaries, not raw output. The summaries carry forward; the work stays behind.

The result: sessions feel longer than the context window suggests. The main agent retains awareness of everything that happened — through summaries — without the raw token cost of everything that was read, searched, and analyzed by sub-agents.

---

## Sources

- Context window sizes from Anthropic model documentation (Claude 3.5/4 series: 200K standard, 1M extended)
- Token estimation: ~4 characters per token for English markdown (industry standard approximation)
- `make context-budget` measures actual character counts and divides by 4

---

*Load what you need. Measure what you load. Leave room to think.*
