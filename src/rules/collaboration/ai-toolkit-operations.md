# AI Toolkit Operations

> How to create, update, and deploy agents, rules, skills, and profiles in the ai-toolkit.
> Primary reference for the Knowledge Manager agent and anyone modifying the knowledge base.

---

## Location

The root of the ai-toolkit repository.

## Source Content Structure

All editable content lives under `src/`:

| Path | What | Format |
|---|---|---|
| `src/agents/{domain}/{name}.md` | Agent definitions | YAML frontmatter + markdown body |
| `src/rules/{category}/{topic}.md` | Knowledge/reference documents | Plain markdown, no frontmatter |
| `src/skills/{skill-name}/SKILL.md` | Task templates | Markdown with frontmatter |
| `src/hooks/{hook-name}.py` | Auto-wired Python scripts | Python |
| `src/mcps.yaml` | MCP server definitions | YAML |
| `src/hooks-meta.yaml` | Hook event bindings | YAML |
| `profiles.yaml` | Profile definitions (root level) | YAML with JSON schema |

---

## Agent Domains

| Domain | Directory | Agents |
|---|---|---|
| `core` | `src/agents/core/` | Architect, Developer, Reviewer, Tester, Security, Writer, Designer, DevOps |

Add your own domains and agents as needed.

## Rule Categories

| Category | Directory | Contents |
|---|---|---|
| `collaboration` | `src/rules/collaboration/` | Git, design patterns, operational constraints, ai-toolkit ops, knowledge management |

Add your own categories as needed (e.g., `data/`, `infra/`, `python/`, `engineering/`).

---

## Workflow: Teach an Agent

### Step 1: Create the rule file

```bash
# New rule
cat > src/rules/{category}/{topic}.md << 'EOF'
# Topic Title

> Source description, author, year.
> How this connects to analysis workflows.

---

## Content here...
EOF
```

Rules are plain markdown. No frontmatter. Organize by topic category.

### Step 2: Reference from agent

Edit the agent's `.md` file. Add a reference line in the header block (the `>` quoted section near the top):

```markdown
> Topic: see `rules/{topic}.md` — brief description of what's in the rule
```

### Step 3: Register in profiles.yaml

For rules that should apply to **all profiles**, add to `global_rules`:

```yaml
global_rules:
  collaboration:
    - my-new-rule    # deploys to every profile
```

For rules specific to **one profile**, add under that profile's `rules`:

```yaml
my-profile:
  rules:
    data:
      - my-new-rule    # only when this profile is active
```

### Step 4: Deploy

```bash
make use-profile PROFILE={active_profile}
```

---

## Workflow: Create a New Profile

### Step 1: Add to profiles.yaml

```yaml
my-profile:
  description: What this profile is for
  rules:
    finance:
      - free-public-data-sources
      - my-rule
  hooks:
    - safety-check
```

**Key rules:**
- `description` is the only required field
- Agents and skills are auto-discovered — no need to list them
- `global_rules` at the top of profiles.yaml deploy to every profile automatically
- Rule keys (e.g., `tools`, `infra`) are arbitrary labels — they don't need to match directory names
- Filenames must be unique repo-wide — the deploy script resolves by recursive search
- Everything deploys flat to `~/.claude/agents/` and `~/.claude/rules/`
- Keep profiles lean — only include what the target workflow needs

### Step 2: Validate and deploy

```bash
make validate                           # Check schema
make use-profile PROFILE=my-profile     # Deploy (removes content from previous profile)
```

---

## Workflow: Update/Amend a Rule

1. Read the existing rule: `src/rules/{category}/{topic}.md`
2. Find the right section to edit
3. Use Edit tool to modify in place — preserve existing structure
4. Deploy: `make use-profile PROFILE={active_profile}`

No re-registration needed if the rule is already in the profile.

---

## Workflow: Create a New Agent

### Step 1: Create the agent file

```markdown
---
name: my-agent-name
description: Use this agent when... Also invoke when the user says '...'
model: sonnet
tools: Read, Write, Edit, Bash, Glob, Grep
color: blue
emoji: "\U0001F916"
version: 1.0.0
opencode_description: Short description for OpenCode.
---

> Rules references here
> More rules references

# Agent Name

You are a specialist in X...
```

**Frontmatter fields:**

| Field | Required | Values |
|---|---|---|
| `name` | Yes | Kebab-case identifier |
| `description` | Yes | When to invoke — include trigger phrases |
| `model` | No | `haiku`, `sonnet`, `opus` (default: session model) |
| `tools` | No | Comma-separated (default: inherit all) |
| `color` | No | `red`, `orange`, `yellow`, `green`, `teal`, `cyan`, `blue`, `indigo`, `violet`, `purple`, `pink`, `gray`, `white` |
| `emoji` | No | Unicode emoji |
| `version` | No | Semver |

### Step 2: Register in profiles.yaml and deploy

```yaml
agents:
  my-domain:
    - my-agent-name
```

---

## Validation

```bash
make validate    # Validates ALL YAML + agent frontmatter
```

Checks:
- `profiles.yaml` against `schemas/profiles.schema.json`
- Agent `.md` frontmatter against `schemas/agent.schema.json`
- `src/mcps.yaml` against `schemas/mcps.schema.json`
- `src/hooks-meta.yaml` against `schemas/hooks-meta.schema.json`
- Platform configs against their schemas

**Agent name format warnings** (e.g., `'My Agent' does not match '^[a-z]...'`) are pre-existing and can be ignored. Profile schema errors must be fixed.

---

## Useful Make Targets

```bash
make list-agents                      # List all agents in src/
make list-rules                       # List all rules in src/
make list-skills                      # List all skills in src/
make list-profiles                    # List all profiles
make show-profile PROFILE=<name>      # Preview a profile's contents
make validate                         # Validate all YAML/frontmatter
make use-profile PROFILE=<name>       # Deploy a profile
make verify                           # Check what's deployed locally
make reset                            # Remove all deployed resources
```

---

## Active Profiles

All profiles deploy all agents and skills automatically. Only rules differ.

| Profile | Purpose | Global Rules | Profile Rules | Total Rules |
|---|---|---|---|---|
| `default` | Full engineering | 4 | 0 | 4 |

Add your own profiles as needed. Switch: `make use-profile PROFILE=<name>`

---

## Cross-References

- See `rules/knowledge-management.md` for how rules and agent knowledge are structured and maintained
