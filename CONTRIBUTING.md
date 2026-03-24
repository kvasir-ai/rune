# Contributing

Welcome to rune. We're glad you're here. Whether you're adding a new agent, writing a rule, or improving a hook, contributions of any size are welcome.

All configuration lives in `src/`. Agents, rules, skills, and hooks are plain files — add yours, register it in a profile, validate, and deploy.

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
| `model` | No | `haiku`, `sonnet`, or `opus` — defaults to session model |
| `tools` | No | Comma-separated list — omit to inherit all |
| `color` | No | Named color: `red`, `blue`, `green`, `purple`, etc. |
| `emoji` | No | Display emoji |
| `version` | No | Semantic version |
| `opencode_description` | No | Shorter description for OpenCode |

**Suggested agent contributions** — these are natural extensions to the shipped team:

| Agent idea | Domain | What it would do |
|---|---|---|
| `go-developer` | `engineering/` | Go-specific patterns, idioms, module conventions |
| `python-developer` | `engineering/` | Python-specific patterns, typing, packaging |
| `data-engineer` | `data/` | Pipeline design, ETL patterns, schema evolution |
| `platform-engineer` | `infra/` | Cloud infrastructure, Terraform, Kubernetes |
| `compliance-reporter` | `regulatory/` | Regulatory checklists, audit trail generation |

Create a new domain directory (`src/agents/data/`, `src/agents/engineering/`) as needed. Agents auto-discover — no registration required.

### Rules

Create `src/rules/<category>/<name>.md` — a plain markdown document. No frontmatter needed.

Rules are reference documents that agents use as context. Organize by topic.

**Suggested rule categories** — each has a README with topic ideas:

| Category | Directory | What goes here |
|---|---|---|
| `collaboration/` | Shipped | Git, planning, ADRs, knowledge management |
| `engineering/` | Empty — needs you | Language conventions, API design, testing strategy, CI/CD |
| `infra/` | Empty — needs you | Cloud services, Terraform, Kubernetes, containers |
| `data/` | Empty — needs you | SQL, data modeling, dbt, streaming, public data sources |
| `regulatory/` | Empty — needs you | GDPR, DORA, AI Act, licensing (see criteria below) |

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

**Suggested skill contributions** — these would complement the existing orchestration:

| Skill idea | What it would do |
|---|---|
| `test-driven-development` | Enforce Red-Green-Refactor cycle before implementation |
| `code-review` | Structured review checklist with severity levels |
| `incident-investigation` | Step-by-step runbook for debugging production issues |
| `git-worktrees` | Safely set up isolated worktrees for parallel feature work |
| `pr-description` | Generate structured pull request descriptions from diffs |
| `compliance-check` | Run regulatory checklists against a codebase or feature |

### Hooks

1. Create `src/hooks/<name>.py` — reads JSON from stdin, optionally prints a response
2. Add event bindings in `src/hooks-meta.yaml`:

```yaml
my-hook:
  description: What this hook does
  events:
    PreToolUse:
      matcher: Bash
      timeout: 10
```

3. Add `my-hook` to a profile's `hooks` list in `profiles.yaml`

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

Then enable: `make enable-mcp MCP=my-mcp`

## Registering in profiles

**Agents and skills** are auto-discovered — they deploy to every profile automatically.

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

Rule group labels (e.g. `collaboration`) are arbitrary — they don't need to match directory names. Filenames must be unique repo-wide.

## Adding regulatory and legal rules

rune ships with collaboration rules, but the framework is designed to absorb domain knowledge — including laws, regulations, standards, and compliance frameworks that help teams build software that is not just great, but also compliant.

### What belongs

| Good fit | Example |
|---|---|
| Laws and regulations that affect software | GDPR, DORA, PSD2, AI Act, SOX IT controls |
| Industry standards with public text | ISO 27001 controls, OWASP Top 10, PCI-DSS requirements |
| Accounting and reporting standards | IFRS summaries, GAAP principles |
| Open data catalogs and public APIs | Eurostat, FRED, ECB SDW, SEC EDGAR, national statistics offices |
| Tax rules relevant to software products | VAT digital services, transfer pricing safe harbors |
| Licensing and IP frameworks | OSI-approved licenses, software patent landscapes |

### Acceptance criteria

Every regulatory or legal rule must satisfy ALL of these:

| Criterion | Why |
|---|---|
| **Publicly available source** | The underlying text must be freely accessible — official gazettes, government websites, standards bodies with public summaries. No paywalled content. |
| **Permissive for commercial use** | Laws and regulations are not copyrightable in most jurisdictions, but standards bodies sometimes restrict reproduction. Confirm the source permits derivative use, or summarize in your own words with attribution. |
| **Broadly applicable** | The rule should help more than one team or project. A regulation affecting all EU software companies — yes. A single company's internal compliance checklist — no. |
| **Actionable for engineers** | Don't just quote the law. Translate it into what engineers must do: checklists, constraints, patterns to follow, patterns to avoid. An agent reading this rule should change its behavior. |
| **Sourced and dated** | Cite the official source with title, article/section numbers, publication date, and a URL. Regulations change — the date tells future readers whether the content is current. |

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

- **Internal company policies** — those are private rules, not FOSS contributions
- **Legal advice or interpretation** — rules state what the law says, not what you should do in a specific case. Add a disclaimer: "This is not legal advice."
- **Paywalled standards reproduced verbatim** — summarize in your own words, cite the source, link to the official purchase page
- **Jurisdiction-specific edge cases** with no general applicability — a tax ruling for one municipality helps nobody
- **Outdated regulations** without marking them as superseded — if you add a rule for a regulation that was amended, note the current version

### Open data sources

Rules that catalog freely available public data are welcome. These help agents find and fetch real data instead of hallucinating it. Criteria:

- The data must be **free to access** (no API key required, or free-tier key available)
- The data must be **legal to use commercially** (check the license — most government statistical data is open)
- The rule should document: **what data is available, API endpoints, update frequency, data format, and known limitations**
- Prefer official sources (Eurostat, FRED, national statistics offices) over third-party aggregators

## Before Submitting

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

## Validation

```bash
make validate    # checks all YAML and agent frontmatter against JSON schemas
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

## Further reading

- [The Edit Distance of Understanding](docs/the-edit-distance-of-understanding.md) — How rune transforms ignorance into insight using the same structural principles as Levenshtein Distance.
- [The Knowledge Creation Cycle](docs/the-knowledge-creation-cycle.md) — How rune's Feed, Shape, Grow lifecycle is grounded in organizational knowledge theory (SECI model + machine dimension).
- [The Context Budget](docs/the-context-budget.md) — Why context management matters, how profiles keep it lean, and how to measure your footprint.
