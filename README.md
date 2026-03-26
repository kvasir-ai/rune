# rune

**Agent orchestration for AI coding tools.**

AI coding agents are powerful but chaotic. Without coordination, they duplicate work, lose context, trash each other's files, and run destructive commands. rune fixes this: **explore** the problem, **plan** the work, **execute** in parallel.

> *The wisest of all shared his knowledge through runes.*

Works with [Claude Code](https://claude.ai/code), [OpenCode](https://github.com/opencode-ai/opencode), and any AI coding tool that reads agent files from a config directory.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-kvasir--ai.github.io%2Frune-blue)](https://kvasir-ai.github.io/rune/)

> **Developer Preview.** Feedback welcome — [open an issue](https://github.com/kvasir-ai/rune/issues).

---

## Quick start

> Requires: [uv](https://docs.astral.sh/uv/), make, Python 3.12+

```bash
git clone https://github.com/kvasir-ai/rune.git && cd rune && make use-profile PROFILE=default
```

Open your AI coding tool in any project. Try:

```
You:      "plan a REST API for user management"
Planner:  [decomposes into tasks with dependencies]
You:      /rune
rune:     Wave 0 — developer + tester in parallel
          Wave 1 — developer wires components
          Wave 2 — reviewer checks everything
          Done. 57% time saved via parallelism.
```

Describe the work. Approve the plan. Type `/rune`.

---

## How it works

Every non-trivial task follows three phases:

```
EXPLORE          →    PLAN             →    EXECUTE
read-only agents      Planner decomposes    independent tasks
gather context        into a dependency     run in parallel waves
in parallel           graph                 with cost tracking
```

**Explore.** Dispatch read-only agents to gather context from different angles. They return summaries — they never write code yet.

**Plan.** The Planner decomposes work into tasks with explicit dependencies. The graph reveals what can run in parallel.

**Execute.** Independent tasks dispatch simultaneously in waves. Each wave's results are summarized into the next wave's prompts. A Judge verifies at the end.

What makes agents "knowledgeable" is not conversation history — it is **pre-loaded rule files**. Each agent starts with domain-specific conventions in its context window. The label alone does nothing; the rules do everything.

Deep dive: **[The Three-Phase Model](docs/the-three-phase-model.md)**

---

## Skills

Slash commands — the primary way you interact with rune.

| Command | What it does |
|---|---|
| `/rune` | Dispatch agents in parallel waves |
| `/rune-demo` | Run showcase DAG examples |
| `/write-plan` | Generate an implementation plan |
| `/judge` | Code review workflow |
| `/judge-audit` | Deep adversarial audit of any output |
| `/judge-panel N` | Multi-perspective review panel |
| `/tw-draft-pr` | Draft a PR description |
| `/tw-release` | Prepare a release — changelog, notes, version, tag |
| `/km-audit` | Audit knowledge base health |
| `/km-onboard` | Analyze repo architecture for onboarding |

---

## The team

rune ships with orchestration agents. You build domain specialists on top.

| Agent | Role |
|---|---|
| **Planner** | Decomposes tasks into dependency graphs |
| **Judge** | Validates correctness and safety across domains |
| **Technical Writer** | Writes docs, ADRs, release notes, agent definitions |
| **Knowledge Manager** | Feeds, shapes, and grows the rule base |

Add your own specialists — developer, tester, security, architect — by duplicating an agent file and loading domain-specific rules. See [AGENTS.md](AGENTS.md).

---

## How it fits together

**Rules** are domain knowledge files that load into agent context windows — coding conventions, infrastructure patterns, compliance requirements. Agents reference the rules relevant to their specialty.

**Profiles** bundle rules for a workflow. `make use-profile PROFILE=security-review` loads compliance rules. Switch profiles in seconds. Deep dive: [The Knowledge Toolkit](docs/the-knowledge-toolkit.md)

**Safety hooks** intercept destructive commands (`rm -rf`, `DROP TABLE`, `git push --force`) before they reach the shell. Configurable via YAML. Deep dive: [The Safety Architecture](docs/the-safety-architecture.md)

---

## Going deeper

| Topic | What you will learn |
|---|---|
| [The Three-Phase Model](docs/the-three-phase-model.md) | Collaboration patterns, DAG format, context management, cost economics |
| [The Knowledge Toolkit](docs/the-knowledge-toolkit.md) | Rules, profiles, the Knowledge Manager, context budget |
| [The Safety Architecture](docs/the-safety-architecture.md) | How hooks block destructive commands |
| [Examples](EXAMPLES.md) | Worked examples with dispatch output |
| [Contributing](CONTRIBUTING.md) | How to add agents, rules, skills, and hooks |

## License

MIT — see [LICENSE](LICENSE).

---

*The team is yours. Teach it everything you know.*
