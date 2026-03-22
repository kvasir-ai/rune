# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in rune, please report it responsibly:

1. **Do NOT open a public GitHub issue** for security vulnerabilities
2. Use [GitHub Security Advisories](https://github.com/rune-agents/rune/security/advisories/new) to report privately
3. Include steps to reproduce, impact assessment, and suggested fix if possible

We will acknowledge receipt within 48 hours and provide a timeline for resolution.

## Scope

rune executes hooks and scripts on your local machine. Security-sensitive areas include:
- **Hooks** (`src/hooks/`) — executed automatically by Claude Code/OpenCode
- **Tool installers** (`tools/`) — download and install third-party binaries
- **MCP configurations** — connect to external services

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |
