# rune

A knowledge absorption toolkit for AI coding agents. Feed your team structured knowledge, shape it into role-specific profiles, and grow it over time.

## Your team

Agents ship in `src/agents/core/`. Add your own alongside them.

| Agent | What they do |
|---|---|
| Architect | System design, API contracts, ADRs |
| Developer | Implementation, features, bug fixes |
| Planner | PMBOK-grounded plans, DAG task breakdown |
| Judge | Supreme validation — cross-domain quality, correctness, safety verdicts |
| Reviewer | Code review, quality gates |
| Tester | Test plans, test suites, coverage |
| Security | Vulnerability assessment, threat modeling |
| Technical Writer | Documentation, ADRs, READMEs |
| Writer | Guides, release notes, changelogs |
| Designer | UI/UX, component design |
| DevOps | Deployment, CI/CD, releases |
| Knowledge Manager | Rule CRUD, audits, profile optimization |

## Knowledge lifecycle

- **Feed** — Drop rules into `src/rules/`. Agents load them as context.
- **Shape** — Group rules into profiles in `profiles.yaml`. One profile per role.
- **Grow** — The Knowledge Manager audits, splits, merges, and fills gaps.

## What ships

| Type | Location |
|---|---|
| Agents | `src/agents/core/` |
| Rules | `src/rules/collaboration/` |
| Skills | `src/skills/` |
| Hooks | `src/hooks/` (safety-check, auto-lint, on-stage-complete) |
| Profiles | `profiles.yaml` |

Use `make list-agents`, `make list-rules`, `make list-skills` to see what is available.

**Skills (SSDLC cycle):**
- Idea: brainstorming
- Plan: writing-plans, writing-clearly-and-concisely
- Execute: rune, executing-plans, dispatching-parallel-agents, subagent-driven-development
- Judge: verification-before-completion, requesting-code-review
- Ship: finishing-development-branch, pr-description
- Meta: rune-examples, skill-creator

## Quick reference

```bash
make use-profile PROFILE=<name>    # deploy a profile
make validate                      # check all YAML + frontmatter
make verify                        # confirm deployed state
make list-agents / list-rules      # browse content
make list-tools                    # see dev tools
make install-tool-<name>           # install a tool
make help                          # all targets
```

## Key conventions

- Never enumerate counts in documentation — use qualitative descriptions and `make list-*` commands instead.
- Rules go in `profiles.yaml` to deploy. Agents and skills auto-discover.
- Filenames must be unique repo-wide — deploy resolves by recursive search.
- Run `make validate` before committing.
- See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.
- See [EXAMPLES.md](EXAMPLES.md) for DAG dispatch showcases.

**Try it:** Say "run rune example 1" to see a full-stack feature dispatched across the team.
