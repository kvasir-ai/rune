# Contributing

Contributions of any size are welcome. Add an agent, write a rule, build a hook — all good.

All content lives in `src/rune-agency/`. Agents, rules, skills, and hooks are plain files. Add yours, register it in a profile, validate, and deploy.

## Adding content

### Agents

Create `src/rune-agency/agents/<phase>/<name>.md` with YAML frontmatter and a system prompt body.

```markdown
---
name: My Agent
description: Use this agent when working on X tasks...
model: sonnet
tools: Read, Write, Edit, Bash, Glob, Grep
color: blue
emoji: "🤖"
version: 1.0.0
---

You are a specialist in X. Your job is to Y.
```

**Frontmatter fields:**

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | Display name (e.g. `My Agent`, `Code Formatter`) |
| `description` | Yes | Tells the orchestrator when to invoke this agent |
| `model` | No | `haiku`, `sonnet`, or `opus`. Defaults to session model |
| `tools` | No | Comma-separated list. Omit to inherit all |
| `color` | No | Named color: `red`, `blue`, `green`, `purple`, etc. |
| `emoji` | No | Display emoji |
| `version` | No | Semantic version |

**Suggested agents** — natural extensions to the shipped team:

| Agent idea | Domain | What it does |
|---|---|---|
| `go-developer` | `engineering/` | Go patterns, idioms, module conventions |
| `python-developer` | `engineering/` | Python patterns, typing, packaging |
| `data-engineer` | `data/` | Pipeline design, ETL patterns, schema evolution |
| `platform-engineer` | `infra/` | Cloud infrastructure, Terraform, Kubernetes |
| `compliance-reporter` | `regulatory/` | Regulatory checklists, audit trail generation |

Create new phase or domain directories under `src/rune-agency/agents/` as needed. Agents auto-discover. No registration required.

### Rules

Create `src/rune-agency/rules/<category>/<name>.md`. Use plain markdown with a `Phase:` banner and no YAML frontmatter.

Rules are reference documents that agents use as context. Organize by topic.

**Suggested categories**:

| Category | Directory | What goes here |
|---|---|---|
| `core/` | Shipped | Git, planning, ADRs, knowledge management |
| `engineering/` | Empty | Language conventions, API design, testing, CI/CD |
| `infra/` | Empty | Cloud services, Terraform, Kubernetes, containers |
| `data/` | Empty | SQL, data modeling, dbt, streaming, public data sources |
| `regulatory/` | Empty | GDPR, DORA, AI Act, licensing |

### Skills

Create `src/rune-agency/skills/<name>/SKILL.md`:

```markdown
---
name: my-skill
description: What this skill does and when to use it.
---

Do the thing described in `$ARGUMENTS`.

## Steps

1. First step
2. Second step
```

### Hooks

1. Create `src/rune-agency/hooks/<name>.py`. It reads JSON from stdin and optionally prints a response.
2. Add event bindings in `src/rune-agency/hooks-meta.yaml`:

```yaml
my-hook:
  description: What this hook does
  events:
    PreToolUse:
      matcher: Bash
      timeout: 10
```

3. Add `my-hook` to a profile's `hooks` list in `profiles.yaml`.

### MCPs

Add a definition to `src/rune-agency/mcps.yaml` (root):

```yaml
my-mcp:
  description: "What this MCP provides"
  claude:
    command: npx
    args: ["-y", "@my/mcp-server@latest"]
    env:
      API_KEY: "${MY_API_KEY}"
```

Then enable it: `rune mcp enable my-mcp`

## Registering in profiles

**Agents and skills** auto-discover. They deploy to every profile automatically.

**Rules** must be registered in `profiles.yaml`:

```yaml
global_rules:
  core:
    - my-universal-rule     # deploys to every profile

my-profile:
  description: "Profile for backend work"
  rules:
    core:
      - dag-execution-format
    engineering:
      - my-custom-rule
  hooks:
    - safety-check
    - auto-lint
```

Rule group labels (e.g. `core`) are arbitrary. They do not need to match directory names. Filenames must be unique repo-wide.

## Before submitting

Run `rune system validate` before opening a PR. It checks:

- `profiles.yaml` against its JSON schema
- All agent `.md` frontmatter against the agent schema
- `src/rune-agency/mcps.yaml` and `src/rune-agency/hooks-meta.yaml` against their schemas

```bash
rune system validate
```

If validation passes, deploy and verify locally:

```bash
rune profile use default
rune system verify
```

## Further reading

- [The Four-Phase Model](docs/the-four-phase-model.md) — The core idea: how agents explore, plan, build, and validate in parallel.
- [The Knowledge Toolkit](docs/the-knowledge-toolkit.md) — Rules, profiles, the Knowledge Manager, and context budgets.
- [The Safety Architecture](docs/the-safety-architecture.md) — How safety hooks block destructive commands.
