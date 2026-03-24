# rune

> **Early preview — friends & family testing.** This is pre-release software shared for feedback. Expect rough edges. If something breaks or confuses, that's the feedback I need.

> *The wisest of all shared his knowledge through runes.*

An agent system for AI-assisted development. Knowledge management, team coordination, and parallel execution — embedded in your coding workflow.

Built by a team trained on the same principles rune provides.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Linux / WSL2 / macOS](https://img.shields.io/badge/platform-Linux%20%7C%20WSL2%20%7C%20macOS-lightgrey)](README.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)
[![OpenCode](https://img.shields.io/badge/OpenCode-compatible-green)](https://opencode.ai)

```bash
git clone https://github.com/rune-agents/rune.git && cd rune && make use-profile PROFILE=default
```

## Starter team

rune ships with a ready-made team. Replace any agent, add your own, delete what you don't need.

| Agent | Role |
|---|---|
| 🏗 Architect | System design, API contracts, architectural decisions |
| 🔧 Developer | Implementation, features, bug fixes |
| 🗺 Planner | Implementation plans, project breakdown, risk assessment |
| 🔍 Reviewer | Code review, quality gates, final approval |
| ⚖️ Judge | Cross-domain validation, correctness, safety verdicts |
| 🧪 Tester | Test plans, test suites, coverage |
| 🔒 Security | Vulnerability assessment, threat modeling |
| ✍️ Technical Writer | Documentation, ADRs, READMEs, API docs |
| ✍️ Writer | Guides, release notes, user-facing content |
| 🎨 Designer | UI/UX, component design, interface planning |
| 🚀 DevOps | Deployment, CI/CD, releases, infrastructure |
| 📚 Knowledge Manager | Rule audits, profile optimization, knowledge lifecycle |

Add your own specialists in `src/agents/`.

## How knowledge absorption works

**Ingest** — Drop raw material into `src/knowledge/`. PDFs, research summaries, extracted docs — anything that is not yet structured for agent consumption. This is the inbox.

**Distill** — The Knowledge Manager reads the inbox and distills raw material into focused, actionable rules in `src/rules/`. Tables, checklists, code blocks — structured knowledge that agents load as context. Never skip the inbox by dumping raw content directly into rules.

**Shape** — Group rules into profiles. A security auditor gets different knowledge than a frontend developer. Profiles control which rules load for which role, keeping context focused and costs low. Switch with one command.

**Grow** — The Knowledge Manager agent audits your knowledge base, detects gaps, flags stale content, splits oversized rules, and integrates new findings from research. Your team's knowledge compounds over time.

Think of it as a second brain for your engineering org — agents absorb your rules and apply them consistently across every task, every time.

## Project management built in

rune ships with PMBOK-grounded project planning, ADR templates, testing strategy, and design patterns baked into the included skills. The `writing-plans` skill breaks down complex features into atomic tasks. The DAG dispatcher executes them in dependency order, running independent tasks in parallel waves. The Architect, Developer, Tester, and Reviewer can work simultaneously on different parts of a feature — coordinated, not sequential.

## Quick start

Install `uv` if you don't have it, then run the one-liner above.

| OS | Install uv |
|---|---|
| macOS | `brew install uv` |
| Linux / WSL | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

Once installed, say `"run rune example 1"` to dispatch a showcase DAG.

## DAG dispatch

Define tasks with dependencies. rune computes waves via topological sort and dispatches each wave in parallel:

```
───────────────────────────────────────────
  DAG DISPATCH PLAN
  Tasks: 7  |  Waves: 3  |  Benefit: 1.8x
───────────────────────────────────────────

  Wave 0  ─── 4 parallel ──────────────────
  🏗️  t1  architect         Design API contract
  🎨  t2  designer          Design UI components
  🔧  t3  developer         Set up database schema
  ✍️  t4  writer            Draft documentation

  Wave 1  ─── 2 parallel ──────────────────
  🔧  t5  developer         Implement API and UI
                              ↳ depends on: t1, t2, t3
  🧪  t6  tester            Write tests
                              ↳ depends on: t1, t3

  Wave 2  ────────────────────────────────
  🔍  t7  reviewer          Final review
                              ↳ depends on: t4, t5, t6

───────────────────────────────────────────
  Critical path: t1 → t5 → t7
  Path length: 3 of 7 tasks (43%)
───────────────────────────────────────────
```

Say `/rune` to dispatch. `"Test this DAG"` for a zero-cost dry run.

See [EXAMPLES.md](EXAMPLES.md) for three full scenarios (1.8x to 3.0x speedup).

## Profiles

A profile controls which rules deploy. All agents and skills deploy to every profile — only the knowledge set changes. The default profile ships lean — run `make context-budget` to measure your footprint. Skills load on demand.

```yaml
# profiles.yaml
my-backend-profile:
  description: Go backend development
  rules:
    collaboration:
      - git-conventions
      - operational-constraints
    engineering:
      - openapi-documentation
  hooks:
    - safety-check
    - auto-lint
```

```bash
make list-profiles                             # see all profiles
make show-profile PROFILE=my-backend-profile   # preview before applying
make use-profile PROFILE=my-backend-profile    # deploy it
```

## Safety hooks

The `safety-check` hook (PreToolUse) blocks before execution:

- `rm -rf` variants (any flag ordering, long-form)
- `DROP TABLE`, `DELETE FROM`, `TRUNCATE`
- Destructive git commands (`--force` push, `reset --hard`, `clean -f`)
- `terraform apply` / `terragrunt apply` targeting production environments
- Authentication commands

The `auto-lint` hook (PostToolUse) runs formatters automatically after file writes.

## License

MIT — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add agents, rules, skills, hooks, MCPs, and tools.

---

*The team is yours. Teach it everything you know.*
