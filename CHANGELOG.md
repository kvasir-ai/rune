# Changelog

All notable changes to rune will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [0.3.0] - 2026-03-26

### Added
- Prefixed skill system — skills owned by core agents: `/judge`, `/judge-audit`, `/judge-panel`, `/tw-draft-pr`, `/tw-release`, `/km-audit`, `/km-onboard`, `/write-plan`, `/rune-demo`
- Judge panel (`/judge-panel N`) — summon 2-5 independent judges for multi-perspective review
- Deep adversarial audit skill (`/judge-audit`)
- Ephemeral site build — GitHub Pages assembled at CI time from `docs/`, no committed HTML/JS
- Documentation site with dark mode, search, sidebar navigation, mermaid diagrams
- Token economics in `/rune` — per-agent token usage, estimated cost, parallelism savings
- AGENTS.md, CODEOWNERS, safety-check test suite

### Changed
- Documentation consolidated around the three-phase model as single authoritative doc
- README rewritten as a sales document — hook, demo, skills table, compressed depth
- Skills renamed from generic to agent-prefixed (release → tw-release, pr-description → tw-draft-pr, audit-docs → km-audit, codebase-onboarding → km-onboard, rune-examples → rune-demo, writing-plans → write-plan)
- Agent names in DAG diagrams use single brackets `[ AGENT ]`
- Core agents updated with skill references and absorbed behaviors

### Removed
- 14 skills demoted to agent behavior or consolidated (brainstorming, executing-plans, verification-before-completion, writing-clearly-and-concisely, skill-creator, subagent-driven-development, finishing-development-branch, dispatching-parallel-agents, requesting-code-review, receiving-code-review, pr-description, release, release-notes, audit-docs)
- Redundant deep-dive docs (DAG dispatch, context budget, edit distance, knowledge creation cycle, knowledge manager) — folded into three-phase model
- Committed `site/` directory — now ephemeral
- Example agents (architect, designer, developer, devops, reviewer, security, tester, writer) — users build their own

## [0.2.0] - 2026-03-24

### Added
- `/release` skill — validate, bump version, update CHANGELOG, commit, and tag
- `/rune` skill — consolidated DAG dispatch (replaces `executing-dag-plans`)
- Configurable safety patterns (`src/hooks/safety-patterns.yaml`)
- Configurable auto-lint rules (`src/hooks/auto-lint-rules.yaml`)
- Model-agnostic peon-ping tiers (`tools/peon-ping/profiles.yaml`) with low/mid/high mapping
- `make context-budget` target — measure token footprint per profile
- Open-source license compliance rule (global)
- Knowledge inbox (`src/knowledge/`) — staging area for raw material before distillation
- Deep dives: edit distance of understanding, knowledge creation cycle, context budget

### Changed
- README rewritten — agent system positioning, install-in-hero, trimmed to sales page
- Safety-check and auto-lint hooks now read from YAML config instead of hardcoded patterns
- Peon-ping profiles externalized to YAML, model-tier mapping supports any model provider
- Knowledge Manager agent now prioritizes `src/knowledge/` inbox before research

### Removed
- `executing-dag-plans` skill (consolidated into `/rune`)

## [0.1.0] - 2026-03-22

### Added
- Core agent team (Architect, Designer, Developer, DevOps, Judge, Knowledge Manager, Planner, Reviewer, Security, Technical Writer, Tester, Writer)
- Collaboration rules (ADRs, AI toolkit operations, DAG execution, design patterns, knowledge management, project planning, open-source license compliance)
- Skills (brainstorming, DAG dispatch, plan execution, plan writing, parallel dispatch, examples, skill creation, verification)
- Hooks (safety-check, auto-lint, on-stage-complete)
- Installable dev tools (rg, fd, fzf, bat, eza, starship, zoxide, uv, yq, rtk, peon-ping)
- Multi-platform support (Claude Code, OpenCode)
- Profile-based deployment system
