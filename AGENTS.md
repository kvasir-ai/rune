# rune — Agent System

This file describes the agent team, the key concepts, and how to help the user. You operate everything through natural language.

## Your team

| Agent | What they do | How to call them |
|---|---|---|
| Planner | Break work into tasks with dependencies | `"plan this feature"`, `"break this down"` |
| Judge | Validate correctness and safety across domains | `"hey judge"`, `"validate this"`, `"second opinion"` |
| Technical Writer | Write docs, ADRs, READMEs, agent definitions | `"document this"`, `"write a README"` |
| Knowledge Manager | Audit rules, optimize profiles, manage knowledge | `"audit the knowledge base"`, `"teach the team about X"` |

These are the orchestration machinery. Add domain specialists (developer, tester, security, reviewer, architect) by duplicating an agent file and loading domain-specific rules.

Agent files live in `src/agents/core/`. Each one is a markdown file with YAML frontmatter and a system prompt.

## The three-phase model

Every non-trivial task follows: **Explore** (gather context) → **Plan** (decompose into a DAG) → **Execute** (dispatch in parallel waves).

- Phase 1: Dispatch read-only agents to research in parallel. They return summaries.
- Phase 2: The Planner decomposes work into tasks with dependencies.
- Phase 3: The dispatcher runs independent tasks simultaneously, wave by wave.

## Key concepts

**Profiles** pick which rules agents load. Switch with `"switch to the security profile"` or `make use-profile PROFILE=<name>`. Help the user pick the right profile for their task.

**Rules** are structured knowledge files in `src/rules/`. They contain conventions, standards, and patterns. Agents read them and follow them. Rules are listed in `profiles.yaml`.

**Skills** are slash commands that start workflows:

| Command | What it does |
|---|---|
| `/rune` | Dispatch agents in parallel waves (from plan or ad-hoc) |
| `/rune-demo` | Run showcase DAG examples |
| `/write-plan` | Generate an implementation plan |
| `/judge` | Code review workflow |
| `/judge-audit` | Deep adversarial audit of any output |
| `/judge-panel N` | Summon N judges for multi-perspective review |
| `/tw-draft-pr` | Draft a PR description |
| `/tw-release` | Prepare a release — changelog, notes, version, tag |
| `/km-audit` | Audit knowledge base health |
| `/km-onboard` | Analyze repo architecture for onboarding |

**Knowledge inbox** (`src/knowledge/`) holds raw material. The Knowledge Manager turns it into rules. Never write directly to `src/rules/`. Always go through the inbox first.

**Safety hooks** block dangerous commands before they run. Edit patterns in `src/hooks/safety-patterns.yaml`. Auto-lint runs formatters after file writes. Edit its config in `src/hooks/auto-lint-rules.yaml`.

## How to help the user

- **Add knowledge**: Tell them to drop files in `src/knowledge/`, then say `"hey knowledge manager, distill this"`.
- **Switch context**: Show them profiles with `make list-profiles` or `"switch to the <name> profile"`.
- **Plan work**: Use the Planner to break it down, then `/rune` to run it.
- **Check work**: Send it to the Judge for review.
- **Measure token usage**: Run `make context-budget`.
- **Learn more**: Point them to the deep dives in `docs/`.

## Deep dives (in docs/)

- [The Three-Phase Model](docs/the-three-phase-model.md) — The core idea: explore, plan, execute, DAG dispatch, context management, cost economics
- [The Knowledge Toolkit](docs/the-knowledge-toolkit.md) — Rules, profiles, Knowledge Manager, context budget
- [The Safety Architecture](docs/the-safety-architecture.md) — How hooks block dangerous commands

## Setup reference

```bash
make use-profile PROFILE=<name>    # deploy a profile
make context-budget                # measure token footprint
make validate                      # check all YAML + frontmatter
make verify                        # confirm deployed state
make list-agents                   # browse agents
make list-rules                    # browse rules
make list-profiles                 # browse profiles
```
