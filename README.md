# rune

> *The wisest of all shared his knowledge through runes.*

A knowledge absorption toolkit for AI coding agents. Grow your team's expertise, orchestrate their work, and keep everyone aligned.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Linux / WSL2 / macOS](https://img.shields.io/badge/platform-Linux%20%7C%20WSL2%20%7C%20macOS-lightgrey)](README.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)
[![OpenCode](https://img.shields.io/badge/OpenCode-compatible-green)](https://opencode.ai)

## Your starting team

Eleven specialists, ready to absorb your knowledge and get to work.

| Agent | Role | Emoji |
|---|---|---|
| Architect | System design, API contracts, architectural decisions | 🏗 |
| Developer | Implementation, features, bug fixes | 🔧 |
| Planner | Implementation plans, project breakdown, risk assessment | 🗺 |
| Reviewer | Code review, quality gates, final approval | 🔍 |
| Tester | Test plans, test suites, coverage | 🧪 |
| Security | Vulnerability assessment, threat modeling | 🔒 |
| Technical Writer | Documentation, ADRs, READMEs, API docs | ✍ |
| Writer | Guides, release notes, user-facing content | ✍ |
| Designer | UI/UX, component design, interface planning | 🎨 |
| DevOps | Deployment, CI/CD, releases, infrastructure | 🚀 |
| Knowledge Manager | Rule CRUD, audits, profile optimization | 📚 |

Add your own specialists in `src/agents/`.

## How knowledge absorption works

**Feed** — Drop reference documents into `src/rules/`. These are structured knowledge that agents load as context when they work. Cover your coding conventions, API standards, compliance requirements, domain expertise, architectural decisions — anything your team needs to know to do the job right.

**Shape** — Group rules into profiles. A security auditor gets different knowledge than a frontend developer. Profiles control which rules load for which role, keeping context focused and costs low. Switch with one command.

**Grow** — The Knowledge Manager agent audits your knowledge base, detects gaps, flags stale content, splits oversized rules, and integrates new findings from research. Your team's knowledge compounds over time.

Think of it as a second brain for your engineering org — agents absorb your rules and apply them consistently across every task, every time.

## Project management built in

rune ships with PMBOK-grounded project planning, ADR templates, testing strategy, and design patterns baked into the included skills. The `writing-plans` skill breaks down complex features into atomic tasks. The DAG dispatcher executes them in dependency order, running independent tasks in parallel waves. The Architect, Developer, Tester, and Reviewer can work simultaneously on different parts of a feature — coordinated, not sequential.

## Quick start

```bash
git clone https://github.com/rune-agents/rune.git
cd rune
make use-profile PROFILE=default   # deploy to Claude Code + OpenCode
make verify                        # confirm what was installed
make list-agents                   # browse available agents
```

**Prerequisites:** `make` and `uv` (`pip install uv` or see [uv docs](https://docs.astral.sh/uv/)).

Try it: say `"run rune example 1"` (or 2, 3) to dispatch a showcase DAG immediately.

## DAG dispatch

Define tasks with dependencies. rune computes waves via topological sort and dispatches each wave in parallel:

```
  Wave 0  ─── 4 parallel ────────────────
  🏗️  architect       Design API contract
  🎨  designer        Design UI components
  🔧  developer       Set up database schema
  ✍️  writer          Draft documentation

  Wave 1  ─── 2 parallel ────────────────
  🔧  developer       Implement API and UI        ↳ t1, t2, t3
  🧪  tester          Write tests                 ↳ t1, t3

  Wave 2  ────────────────────────────────
  🔍  reviewer        Final review                ↳ t4, t5, t6
```

Say `"Execute this DAG plan"` to run it. `"Test this DAG"` for a zero-cost dry run.

See [EXAMPLES.md](EXAMPLES.md) for three full scenarios (1.8x to 3.0x speedup).

## Project structure

```
rune/
├── src/
│   ├── agents/              # Agent .md files — add your own
│   ├── rules/               # Reference documents — add your own
│   ├── skills/              # Task templates (6 included)
│   ├── hooks/               # Safety hooks (3 included)
│   ├── hooks-meta.yaml      # Hook event bindings
│   └── mcps.yaml            # MCP server definitions
├── tools/                   # 11 dev tool install/uninstall scripts
├── schemas/                 # JSON schemas for all config files
├── platforms/               # Claude Code + OpenCode platform config
├── profiles.yaml            # Which rules deploy to each profile
└── Makefile
```

## Profiles

A profile controls which rules deploy. All agents and skills deploy to every profile — only the knowledge set changes.

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

## Adding your content

| What | Where |
|---|---|
| New agent | `src/agents/{domain}/my-agent.md` |
| New rule document | `src/rules/{category}/my-rule.md` |
| New skill | `src/skills/my-skill/SKILL.md` |
| New hook | `src/hooks/my-hook.py` + register in `src/hooks-meta.yaml` |
| New MCP | entry in `src/mcps.yaml` |

Register rules in `profiles.yaml` to deploy them. Agents and skills are auto-discovered. Run `make validate` before committing.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.

## Tools

11 dev tools with idempotent install/uninstall scripts. Separate from profiles — install once, they stay.

```bash
make list-tools               # see available tools and install status
make install-tool-rg          # install ripgrep
make install-tool-uv          # install uv
```

Available: `rg`, `fd`, `fzf`, `bat`, `eza`, `starship`, `zoxide`, `uv`, `yq`, `rtk` (token-optimized CLI proxy for Claude Code), `peon-ping` (model-pack rotation with audio cues).

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

**rune** is the open-source foundation. Something bigger is coming.
