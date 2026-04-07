Phase: Core

# Rune Agency Operations

> How to create, update, and deploy agents, rules, skills, and profiles in the Rune Agency.
> Primary reference for the Knowledge Manager agent and anyone modifying the knowledge base.

---

## Location

The root of the rune repository.

## Source Content Structure

All editable content lives under `src/rune-agency/`:

| Path | What | Format |
|---|---|---|
| `src/rune-agency/agents/{phase}/{name}.md` | Agent definitions | YAML frontmatter + markdown body |
| `src/rune-agency/rules/{phase}/{topic}.md` | Knowledge/reference documents | Plain markdown with `Phase:` banner, no YAML frontmatter |
| `src/rune-agency/skills/{phase}/{skill-name}/SKILL.md` | Task templates | Markdown with frontmatter |
| `src/rune-agency/hooks/{phase}/{name}.py` | Auto-wired Python hook scripts | Python |
| `src/rune-agency/hooks/{phase}/*.yaml` | Hook companion config such as pattern or formatter rules | YAML |
| `src/rune-agency/mcps.yaml` | MCP server definitions | YAML |
| `src/rune-agency/hooks-meta.yaml` | Hook event bindings | YAML |
| `profiles.yaml` | Shared profile definitions (root level) | YAML with JSON schema |

---

## Content Organization

Rune Agency uses the Four-Phase Model directly in the filesystem. Put content
under the phase that owns it.

| Resource | Directory |
|---|---|
| Agents | `src/rune-agency/agents/<phase>/` |
| Rules | `src/rune-agency/rules/<phase>/` |
| Skills | `src/rune-agency/skills/<phase>/` |
| Hooks | `src/rune-agency/hooks/<phase>/` |

Shared rules that truly apply everywhere may still live under
`src/rune-agency/rules/core/`, but phase-specific doctrine belongs under the
owning phase.

## Canonical Artifacts

| Surface | Use |
|---|---|
| `docs/plans/` | tracked execution plans intended for review or reuse |
| `docs/decisions/` | tracked ADRs |
| `.rune/` | ephemeral session memory, ledgers, draft packets |
| `src/rune-agency/knowledge/` | durable inputs awaiting promotion |

Never introduce `docs/adrs/` as a second canon.

## Rule Document Shape

Every rule should start with this structure:

```markdown
Phase: Core

# Rule Title

> One or two lines describing scope and intended use.

---
```

Use YAML frontmatter in agents and skills, not in rules.

---

## Workflow: Teach an Agent

### Step 1: Create the rule file

```bash
mkdir -p src/rune-agency/rules/{phase}
```

Create the file with the canonical header shape above. Rules stay as plain
markdown; do not add YAML frontmatter.

### Step 2: Reference from agent

Edit the agent's `.md` file. Add a reference line in the header block:

```markdown
> Topic: see src/rune-agency/rules/{phase}/{topic}.md — brief description of what's in the rule
```

### Step 3: Register in a profile

Add to `profiles.yaml`. For rules that should apply to **all profiles**, add to `global_rules`:

```yaml
global_rules:
  core:
    - core/my-new-rule    # deploys to every profile
```

For rules specific to **one phase or profile**, add under that profile's `rules`:

```yaml
my-profile:
  rules:
    plan:
      - plan/my-new-rule    # only when this profile is active
```

### Step 4: Deploy

```bash
rune profile use {active_profile}
```

---

## Workflow: Create a New Profile

### Step 1: Define the profile

Add to `profiles.yaml`.

```yaml
my-profile:
  description: What this profile is for
  rules:
    explore:
      - explore/my-rule
  hooks:
    - core/safety-check
```

### Step 2: Validate and deploy

```bash
rune system validate          # Check schema
rune profile use my-profile   # Deploy
```

---

## Workflow: Create a New Agent

### Step 1: Create the agent file

```markdown
---
name: my-agent-name
description: Use this agent when...
model: sonnet
tools: Read, Write, Edit, Bash, Glob, Grep
color: blue
emoji: "🤖"
version: 1.0.0
---

# Agent Name

You are a specialist in X...
```

### Step 2: Deploy

```bash
rune profile reapply
```

---

## Workflow: Create Or Update A Hook

### Step 1: Create the script in the owning phase

```bash
mkdir -p src/rune-agency/hooks/{phase}
```

Create the hook script at:

```text
src/rune-agency/hooks/{phase}/{hook-name}.py
```

If the hook needs editable runtime data, keep the companion YAML in the same
phase directory.

### Step 2: Register the binding

Add the event wiring to `src/rune-agency/hooks-meta.yaml`:

```yaml
core/my-hook:
  description: Short behavior summary
  events:
    Notification:
      timeout: 10
```

### Step 3: Wire the hook into a profile

```yaml
my-profile:
  hooks:
    - core/my-hook
```

### Step 4: Validate and redeploy

```bash
rune system validate
rune profile use {active_profile}
```

---

## Useful CLI Commands

```bash
rune resource list        # List deployed resources
rune resource skills      # List deployed skills
rune profile list         # List all profiles
rune system validate      # Validate YAML/frontmatter and configuration
rune profile use <name>   # Deploy a profile
rune profile reapply      # Re-deploy the active profile
rune system verify        # Check what's deployed locally
rune reset                # Remove all deployed resources
```

---

## Cross-References

- See `src/rune-agency/rules/explore/knowledge-management.md` for how rules and agent knowledge are structured and maintained
- See `src/rune-agency/rules/core/hook-runtime-contract.md` for hook bundle and verification doctrine
