# Rune Agency — Phase Agents

The **Rune Agency** team operates as an orchestrated group of experts within the Four-Phase Model. Agents never work in isolation; they are deployed within **Profiles** to provide specialized logic for the current task.

## The Team

| Agent | Role in the Agency | Activation Phrase |
|---|---|---|
| **Planner** | Decomposes work into atomic DAG tasks | `"plan this feature"`, `"break this down"` |
| **Judge** | Validates correctness and safety across domains | `"hey judge"`, `"validate this"`, `"second opinion"` |
| **Engineer** | End-to-end implementation (Dev + Security + QA) | `"implement this"`, `"fix the bug"`, `"refactor this"` |
| **Researcher** | Lightweight context gathering and synthesis | `"research this"`, `"where is X defined"`, `"find patterns"` |
| **Technical Writer** | Writes docs, ADRs, READMEs, agent definitions | `"document this"`, `"write a README"` |
| **Knowledge Manager** | Audits rules, optimizes profiles, manages knowledge | `"audit the knowledge base"`, `"teach the team about X"` |

All agents are defined in `src/rune-agency/agents/<phase>/` as Markdown files with YAML frontmatter.

## The Four-Phase Model

Every non-trivial task follows the **Four-Phase Model**: **Explore** (gather context) → **Plan** (decompose into a DAG) → **Build** (dispatch in parallel waves) → **Validate** (verify output before shipping).

- **Phase 1: Explore** — Dispatch read-only agents to research in parallel. They return summaries.
- **Phase 2: Plan** — The Planner decomposes work into tasks with dependencies.
- **Phase 3: Build** — The dispatcher runs independent tasks simultaneously, wave by wave.
- **Phase 4: Validate** — The Judge and validation workflows verify output before it ships.

See [README.md](/mnt/e/development/ai/kvasir/foss/README.md) and [site/index.html](/mnt/e/development/ai/kvasir/foss/site/index.html) for the rendered lifecycle and onboarding flow.

## Key Concepts

**Profiles** pick which rules agents load. Switch with `"switch to the security profile"` or `rune profile use <name>`.

**Rules** are structured knowledge files in `src/rune-agency/rules/`. They contain conventions, standards, and patterns.

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
| `/km-explore` | Analyze repo architecture for onboarding |

**Knowledge Inbox** (`src/rune-agency/knowledge/`) holds durable raw material. `.rune/` holds ephemeral workflow memory; the Knowledge Manager turns durable findings into rules.

**Hooks** are phase-scoped runtime guardrails and helpers. Treat the hook script, `src/rune-agency/hooks-meta.yaml`, profile wiring, and any companion config as one change surface. Safety patterns live in `src/rune-agency/hooks/core/safety-patterns.yaml`.

**Claude Workflow Layer** uses `.rune/session-state.json` when a workflow is active. The schema lives in [schemas/rune-session-state.schema.json](/mnt/e/development/ai/kvasir/foss/schemas/rune-session-state.schema.json).

## How to Help the User

- **Add Knowledge**: Drop files in `src/rune-agency/knowledge/`, then say `"hey knowledge manager, distill this"`.
- **Switch Context**: Show profiles with `rune profile list` or `"switch to the <name> profile"`.
- **Plan Work**: Use the Planner to break it down, then `/rune` to run it.
- **Check Work**: Send it to the Judge for review.

## Further Reading

- [README.md](/mnt/e/development/ai/kvasir/foss/README.md) — quick start and project positioning.
- [site/index.html](/mnt/e/development/ai/kvasir/foss/site/index.html) — generated public docs.
- `src/rune-agency/agents/<phase>/` — agent definitions and role boundaries.
- `src/rune-agency/rules/<phase>/` — collaboration, planning, and validation doctrine.
