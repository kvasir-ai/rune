---
description: "Summon a panel of N judges for multi-perspective review. Each judge evaluates independently, then a synthesis produces the final verdict. Use: /judge-panel 3 or /judge-panel 5"
argument-hint: <N> (number of judges, 2-5)
user_invocable: true
---

# Judge Panel

Summon a panel of judges to review work from multiple independent perspectives. Each judge evaluates the same artifact but focuses on a different dimension. The panel then synthesizes a combined verdict.

## Parse Arguments

Extract `N` from `$ARGUMENTS`. Must be an integer between 2 and 5. Default to 3 if not provided or invalid.

## Determine What to Review

Ask the user what to review, or use the most recent significant output in the conversation (a plan, code change, design decision, or agent response).

## Assign Perspectives

Each judge gets a distinct focus. Assign based on panel size:

**Panel of 2:**
1. **Correctness Judge** — technical accuracy, code quality, edge cases
2. **Safety Judge** — security, data protection, destructive operations, failure modes

**Panel of 3:**
1. **Correctness Judge** — technical accuracy, code quality, edge cases
2. **Safety Judge** — security, data protection, destructive operations, failure modes
3. **Completeness Judge** — missing requirements, untested paths, documentation gaps

**Panel of 4:**
1. **Correctness Judge** — technical accuracy, code quality, edge cases
2. **Safety Judge** — security, data protection, destructive operations, failure modes
3. **Completeness Judge** — missing requirements, untested paths, documentation gaps
4. **Architecture Judge** — design consistency, separation of concerns, maintainability

**Panel of 5:**
1. **Correctness Judge** — technical accuracy, code quality, edge cases
2. **Safety Judge** — security, data protection, destructive operations, failure modes
3. **Completeness Judge** — missing requirements, untested paths, documentation gaps
4. **Architecture Judge** — design consistency, separation of concerns, maintainability
5. **Devil's Advocate** — challenges assumptions, argues the opposite position, stress-tests reasoning

## Dispatch

Dispatch all N judges in parallel as subagents. Each receives:
- The artifact to review
- Their assigned perspective
- Instructions to produce findings in this format:

```
PERSPECTIVE: [judge role]
VERDICT: PASS / CONCERNS / FAIL
FINDINGS:
- [finding with specific location and recommendation]
CONFIDENCE: [HIGH / MEDIUM / LOW]
```

## Synthesize

After all judges return, produce the combined verdict:

```
PANEL VERDICT: APPROVED / APPROVED WITH WARNINGS / BLOCKED
PANEL SIZE: N judges

UNANIMOUS:
- [findings all judges agree on]

SPLIT:
- [findings where judges disagree — state both positions]

PER-JUDGE SUMMARY:
| Judge | Verdict | Key Finding |
|---|---|---|
| Correctness | PASS | ... |
| Safety | CONCERNS | ... |
| ... | ... | ... |

RECOMMENDATION: [single clear action for the user]
```

## Rules

- Judges are independent — they do not see each other's output
- A single FAIL from any judge escalates to BLOCKED (unless other judges provide strong counter-evidence)
- The synthesis must not soften findings — if a judge found a critical issue, it stays critical
- The Devil's Advocate (panel of 5) is explicitly adversarial — their job is to challenge, not agree
