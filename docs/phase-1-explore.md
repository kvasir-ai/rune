# Phase 1: Explore

> Understand the problem before committing to a plan. Dispatch read-only agents in parallel to gather context from different angles.

---

## The Core Idea

A single generalist agent doing everything is like a single developer who is simultaneously a database engineer, security auditor, frontend developer, and infrastructure architect. They can do each job, but not as well as a specialist — and certainly not in parallel.

**Knowledgeable agents** are specialists. Each one carries domain-specific rules, patterns, and conventions in its context window. A developer agent knows your coding conventions, module structure, and testing patterns. A security agent knows compliance requirements and threat modeling. They don't need to learn — they arrive with expertise loaded.

What makes agents "knowledgeable" is not conversation history — it is **pre-loaded rule files**. Each agent starts with domain-specific conventions, patterns, and checklists already in its context window before the first prompt arrives. This is what separates a named agent from "the same LLM with a different label" — the label alone does nothing; the rules do everything.

---

## How Exploration Works

Before doing anything, understand the problem. Dispatch read-only agents in parallel to gather context from different angles. They research, analyze, and return summaries — they never write code.

```
════════════════════════════════════════════════
  FAN-OUT EXECUTION
  Agents: 4  |  Waves: 2  |  Type: research
════════════════════════════════════════════════

  Wave 0 ──── parallel ───────────────────────
  #1  DEVELOPER             Read existing API structure
  #2  RESEARCHER            Check upstream data sources
  #3  SECURITY              Assess compliance requirements
  #4  TESTER                Review current test coverage

  Wave 1 ──── sequential ─────────────────────
  #5  JUDGE                 Synthesize all findings
                             → #1, #2, #3, #4

════════════════════════════════════════════════
```

**Why this works:** Four agents reading four different parts of the codebase simultaneously. Each returns a 2-3 sentence summary. The Judge merges them into a unified picture. Total wall time: ~2 minutes. Sequential equivalent: ~8 minutes.

**Key principle:** Subagents are context collectors, not implementers. They read and report. The main conversation (or a Planner) takes their findings and builds the plan.

---

## Context Management: The Hidden Efficiency

The biggest cost in LLM-based systems is not compute — it is context. Every file read, every log line, every query result that enters a context window displaces space for reasoning.

Subagents solve this by making context **ephemeral**. Each subagent starts with a fresh context window. It reads as much as it needs, does its analysis internally, and returns only a distilled summary. When the subagent completes, its heavy context dies. Only the summary survives in the parent.

**The core insight: the main context window never sees the raw material. It sees only the finished product.**

```
Subagent internally: 300K tokens (file reads, log parsing, query results, dead ends)
  → Returns to parent: "The staging model has a NULL handling bug in the price
     column. Line 47 passes through NULLs that should be filtered."

Parent receives: 42 tokens. Not 300K.
```

| Subagents Dispatched | Total Work Done | Main Context Growth | Budget Used |
|---|---|---|---|
| 1 | ~130K tokens | ~100 tokens | Negligible |
| 5 | ~650K tokens | ~500 tokens | Under 0.1% of 1M window |
| 10 | ~1.3M tokens | ~1,000 tokens | 0.1% |
| 20 | ~2.6M tokens | ~2,000 tokens | 0.2% |

This is what makes deep DAGs practical. A 12-wave, 20-task DAG can dispatch agents that collectively process millions of tokens. The main context holds only the accumulated summaries and stays fast, focused, and accurate from the first wave to the last.

---

*Next: [Phase 2: Plan](phase-2-plan.md) — decompose the findings into a dependency graph.*
