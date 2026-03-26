# Security Policy

## Safety Architecture

rune ships with safety hooks that block destructive commands (`rm -rf`, `DROP TABLE`, `git push --force`) before they reach the shell. Patterns are configurable via `src/hooks/safety-patterns.yaml` and covered by a test suite (`python3 tests/test-safety-check.py`).

The safety hook is a seatbelt, not a security boundary — it catches common accidental destructive commands that LLM agents generate. OS permissions, sandboxing, and CI/CD gates handle the layers above and below.

Full specification: **[The Safety Architecture](docs/the-safety-architecture.md)**

## Reporting a Vulnerability

If you find a security vulnerability in rune:

1. **Do NOT open a public GitHub issue**
2. Use [GitHub Security Advisories](https://github.com/kvasir-ai/rune/security/advisories/new) to report privately
3. Include steps to reproduce, impact assessment, and suggested fix if possible

We acknowledge receipt within 48 hours and provide a resolution timeline.

## Scope

rune executes hooks and scripts on your local machine. Security-sensitive areas:

- **Hooks** (`src/hooks/`) — executed automatically by Claude Code/OpenCode
- **Tool installers** (`tools/`) — download and install third-party binaries
- **MCP configurations** — connect to external services

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.2.x   | Yes       |
| 0.1.x   | Yes       |
