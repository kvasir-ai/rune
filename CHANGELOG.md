# Changelog

All notable changes to rune will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

## [0.3.0] - 2026-03-25

### Added
- Documentation site — single-page app with dark mode, search, sidebar navigation, mermaid diagrams, and copy-to-clipboard
- GitHub Pages deployment via artifact workflow
- CODEOWNERS file for review routing
- Token economics in `/rune` — per-agent token usage, estimated cost, wall time vs CPU time, and parallelism savings
- Deep dive: The DAG Dispatch — full user journey from idea to running DAG
- Deep dives: The Knowledge Manager, The Safety Architecture
- AGENTS.md — agent roster reference
- Site deep dives sync from docs/*.md via marked.js
- Cross-references on all six deep dives
- Safety-check test suite

### Changed
- README restructured: 30-second demo first, quick start second, interactions before roster
- Developer Preview label replaces Incubating
- Works-with compatibility line added (Claude Code, OpenCode)
- Site sidebar reorganized into Getting Started, Core, Advanced groups
- All three EXAMPLES.md scenarios include token economics
- /rune SKILL.md aligned as single source of truth
- ai-toolkit-operations rule renamed to toolkit-operations
- CONTRIBUTING.md, SECURITY.md, CLAUDE.md refreshed

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
