# Contributing

Contributions of any size are welcome. Add an agent, write a rule, build a hook —all good.

All content lives in `src/`. Agents, rules, skills, and hooks are plain files. Add yours, register it in a profile, validate, and deploy.

## Adding content

### Agents

Create `src/agents/<category>/<name>.md` with YAML frontmatter and a system prompt body.

```markdown
---
name: My Agent
description: Use this agent when working on X tasks...
model: sonnet
tools: Read, Write, Edit, Bash, Glob, Grep
color: blue
emoji: "\U0001F916"
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
| `opencode_description` | No | Shorter description for OpenCode |

**Suggested agents** —natural extensions to the shipped team:

| Agent idea | Domain | What it does |
|---|---|---|
| `go-developer` | `engineering/` | Go patterns, idioms, module conventions |
| `python-developer` | `engineering/` | Python patterns, typing, packaging |
| `data-engineer` | `data/` | Pipeline design, ETL patterns, schema evolution |
| `platform-engineer` | `infra/` | Cloud infrastructure, Terraform, Kubernetes |
| `compliance-reporter` | `regulatory/` | Regulatory checklists, audit trail generation |

Create new domain directories (`src/agents/data/`, `src/agents/engineering/`) as needed. Agents auto-discover. No registration required.

### Rules

Create `src/rules/<category>/<name>.md`. Plain markdown. No frontmatter.

Rules are reference documents that agents use as context. Organize by topic.

**Suggested categories** —each has a README with topic ideas:

| Category | Directory | What goes here |
|---|---|---|
| `collaboration/` | Shipped | Git, planning, ADRs, knowledge management |
| `engineering/` | Empty | Language conventions, API design, testing, CI/CD |
| `infra/` | Empty | Cloud services, Terraform, Kubernetes, containers |
| `data/` | Empty | SQL, data modeling, dbt, streaming, public data sources |
| `regulatory/` | Empty | GDPR, DORA, AI Act, licensing (see criteria below) |

### Skills

Create `src/skills/<name>/SKILL.md`:

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

**Suggested skills:**

| Skill idea | What it does |
|---|---|
| `test-driven-development` | Enforce Red-Green-Refactor cycle before implementation |
| `code-review` | Structured review checklist with severity levels |
| `incident-investigation` | Step-by-step runbook for debugging production issues |
| `git-worktrees` | Set up isolated worktrees for parallel feature work |
| `pr-description` | Generate structured pull request descriptions from diffs |
| `compliance-check` | Run regulatory checklists against a codebase or feature |

### Hooks

1. Create `src/hooks/<name>.py`. It reads JSON from stdin and optionally prints a response.
2. Add event bindings in `src/hooks-meta.yaml`:

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

Add a definition to `src/mcps.yaml`:

```yaml
my-mcp:
  description: "What this MCP provides"
  claude:
    command: npx
    args: ["-y", "@my/mcp-server@latest"]
    env:
      API_KEY: "${MY_API_KEY}"
  opencode:
    type: local
    command: ["npx", "-y", "@my/mcp-server@latest"]
    environment:
      API_KEY: "${MY_API_KEY}"
```

Then enable it: `make enable-mcp MCP=my-mcp`

## Registering in profiles

**Agents and skills** auto-discover. They deploy to every profile automatically.

**Rules** must be registered in `profiles.yaml`:

```yaml
global_rules:
  collaboration:
    - my-universal-rule     # deploys to every profile

my-profile:
  description: "Profile for backend work"
  rules:
    collaboration:
      - dag-execution-format
    engineering:
      - my-custom-rule
  hooks:
    - safety-check
    - auto-lint
```

Rule group labels (e.g. `collaboration`) are arbitrary. They do not need to match directory names. Filenames must be unique repo-wide.

## Adding regulatory and legal rules

rune ships with collaboration rules. The framework is built to absorb domain knowledge —including laws, regulations, standards, and compliance frameworks.

### What belongs

| Good fit | Example |
|---|---|
| Laws and regulations that affect software | GDPR, DORA, PSD2, AI Act, SOX IT controls |
| Industry standards with public text | ISO 27001 controls, OWASP Top 10, PCI-DSS requirements |
| Accounting and reporting standards | IFRS summaries, GAAP principles |
| Open data catalogs and public APIs | Eurostat, FRED, ECB SDW, SEC EDGAR |
| Tax rules relevant to software products | VAT digital services, transfer pricing safe harbors |
| Licensing and IP frameworks | OSI-approved licenses, software patent landscapes |

### Acceptance criteria

Every regulatory or legal rule must satisfy ALL of these:

| Criterion | Why |
|---|---|
| **Publicly available source** | The underlying text must be freely accessible. Official gazettes, government websites, standards bodies with public summaries. No paywalled content. |
| **Permissive for commercial use** | Laws are not copyrightable in most jurisdictions. Standards bodies sometimes restrict reproduction. Confirm the source permits derivative use, or summarize in your own words with attribution. |
| **Broadly applicable** | The rule should help more than one team or project. A regulation affecting all EU software companies —yes. A single company's internal checklist —no. |
| **Actionable for engineers** | Do not quote the law. Translate it into what engineers must do: checklists, constraints, patterns to follow, patterns to avoid. An agent reading this rule should change its behavior. |
| **Sourced and dated** | Cite the official source with title, article/section numbers, publication date, and a URL. Regulations change. The date tells future readers whether the content is current. |

### Structure template

```markdown
# Regulation/Standard Name

> Source: Official Name, Article/Section X, publication date.
> URL: https://official-source.example.com/...
> Applicability: Who this affects and when.
> Connection to workflows: How this shapes engineering decisions.

---

## Summary

2-3 sentences: what this regulation requires, in plain language.

## Requirements for Engineers

| Requirement | What to do | What NOT to do |
|---|---|---|
| Data residency (GDPR Art. 44-49) | Store EU personal data in EU regions | Transfer to US without adequacy decision |
| ... | ... | ... |

## Checklists

- [ ] Actionable checklist items an agent can verify

## Cross-References

- See `rules/related-topic.md`
```

### What does NOT belong

- **Internal company policies** —those are private rules, not FOSS contributions
- **Legal advice or interpretation** —rules state what the law says, not what you should do in a specific case. Add a disclaimer: "This is not legal advice."
- **Paywalled standards reproduced verbatim** —summarize in your own words, cite the source, link to the official purchase page
- **Jurisdiction-specific edge cases** with no general applicability
- **Outdated regulations** without marking them as superseded

### Open data sources

Rules that catalog freely available public data are welcome. These help agents find and fetch real data instead of hallucinating it. Criteria:

- The data must be **free to access** (no API key required, or free-tier key available)
- The data must be **legal to use commercially** (check the license)
- The rule should document: **what data is available, API endpoints, update frequency, data format, and known limitations**
- Prefer official sources (Eurostat, FRED, national statistics offices) over third-party aggregators

## Before submitting

Run `make validate` before opening a PR. It checks:

- `profiles.yaml` against its JSON schema
- All agent `.md` frontmatter against the agent schema
- `src/mcps.yaml` and `src/hooks-meta.yaml` against their schemas

```bash
make validate
```

If validation passes, deploy and verify locally:

```bash
make use-profile PROFILE=default
make verify
```

## Useful targets

```bash
make list-agents
make list-rules
make list-skills
make show-profile PROFILE=<name>    # preview before deploying
make use-profile PROFILE=<name>     # deploy
make verify                         # check deployed state
```

## Formatting Reference

How the dispatch output is styled. Useful if you want to customize the look or contribute new display formats.

### Frame Styles

| Where used | Character | Width | Meaning |
|---|---|---|---|
| Plans and reports | `───` (light line) | 43 chars | Structure and results. Nothing is running. |
| Wave banners | `═══` (double line) | 43 chars | Work is happening right now. |

### Task Row Formats

| Where used | Format |
|---|---|
| Before dispatch | `{emoji}  {id}  {agent}  {description}` |
| During dispatch | `{emoji}  {id} → {agent}  {description}` |
| Final report | `{emoji}  {id}  {agent}  {status} {summary}` |

The `→` arrow only appears during execution. It means "this agent is working on this task right now."

### Status Icons

| Icon | Meaning |
|---|---|
| ✅ | Task finished successfully |
| ❌ | Task failed |
| ⛔ | Blocked because a dependency failed |
| ⏭️ | Skipped by the user |

### History

Every dispatch saves a record to `.rune/` in the project root. This folder is gitignored by default.

```
.rune/
  2026-03-23T10-00-00-full-stack-feature.yaml
  2026-03-23T11-00-00-microservice-migration.yaml
  2026-03-23T14-00-00-cross-cloud-deploy.yaml
```

These files contain summaries only. No raw agent output is saved.

## Further reading

- [The Three-Phase Model](docs/the-three-phase-model.md) — The core idea: how agents explore, plan, and execute in parallel. Includes DAG dispatch, context injection, and token economics.
- [The Knowledge Toolkit](docs/the-knowledge-toolkit.md) — Rules, profiles, the Knowledge Manager, and context budgets.
- [The Safety Architecture](docs/the-safety-architecture.md) — How safety hooks block destructive commands and defense-in-depth positioning.
