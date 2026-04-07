---
phase: validate
description: Draft a pull request description for completed work. Communicates the what and why at a system behavior level, not implementation details.
user_invocable: true
---

# Draft PR Description

Shared contract: apply `src/rune-agency/skills/core/skill-contract/SKILL.md`
before following the phase-specific steps below.

## Role

You are a Staff Engineer writing a PR description for peer review. Your audience is other engineers who need to understand the change's purpose, not its code details.

## Rules

- Describe the feature/change at a business or system behavior level
- Start with the primary intent (e.g., "Implement X", "Fix Y", "Refactor Z")
- Reference relevant design docs or ADRs if they exist
- Mention behavioral side effects only if they affect other systems or workflows
- Use active voice and present tense
- Bullet points over prose, bold primary subjects, no fluff

## Process

1. Run `git diff main...HEAD --stat` to identify changed files
2. Run `git log main..HEAD --oneline` to see commit history
3. Scan for referenced ADRs, design docs, or ticket IDs in commits or branch name
4. Synthesize the changes into a structured summary
5. Output only the Summary section in markdown

## Output Format

```markdown
## Summary

- **[Primary change]** — [what it does and why]
- **[Secondary change]** — [what it does and why]
- **[Side effect]** — [what else is affected]
```

## Anti-Patterns

- NEVER list individual files, functions, or code changes
- NEVER include a "Test Plan" or "What was tested" section
- NEVER copy-paste commit messages as the description
- NEVER mention logging, metrics, or observability unless it's the core purpose of the PR
