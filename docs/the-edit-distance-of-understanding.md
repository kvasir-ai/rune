# The Edit Distance of Understanding

> How rune transforms ignorance into insight using the same principles as Levenshtein Distance.

---

## The Observation

[Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance) measures the minimum number of single-character edits — insertions, deletions, substitutions — needed to transform one string into another. It is the foundational algorithm behind spell-checkers, DNA sequence alignment, and fuzzy search.

rune transforms a system's state of understanding from "I know nothing about this task" to "here is the answer, verified by independent reviewers." It does this through waves of coordinated agent dispatches, where each wave builds on the results of the previous one.

The structural parallel is worth examining.

---

## The Mapping

### State Transformation

In Levenshtein, you start with a source string and end with a target string. Every cell in the dynamic programming matrix represents an intermediate state — a partial transformation.

In rune, you start with a **knowledge gap** (the user's question or task) and end with a **verified answer**. Every wave represents an intermediate state — a partial understanding that feeds the next wave.

```
Levenshtein:  "kitten" → "sitting"   (3 edits)
rune:         ignorance → verified answer   (N waves)
```

Both compute the minimum transformation path.

### The Operations

| Levenshtein    | rune                                               | What It Does                                           |
| -------------- | -------------------------------------------------- | ------------------------------------------------------ |
| **Insert**     | A wave adds new knowledge that didn't exist before | An agent researches a topic and surfaces findings      |
| **Delete**     | A wave discards a wrong assumption                 | The Judge identifies a flawed premise and removes it   |
| **Substitute** | A wave replaces an approximation with precision    | A first-pass estimate is refined by a specialist agent |

Each wave in a rune dispatch is an edit operation on the collective understanding. The system gets closer to the target state with every wave.

### Optimal Substructure

Levenshtein uses dynamic programming because the problem has **optimal substructure**: the best solution to the full problem is composed of the best solutions to its subproblems. You never need to recompute a cell — once computed, it is final.

rune exhibits the same property. Wave 0 establishes base knowledge. Wave 1 consumes Wave 0's results — it never re-researches what Wave 0 already established. The **context summaries** passed between waves are the equivalent of the memoized DP cells: compressed, final, and never recomputed.

```
DP cell (i, j) = optimal edit distance for source[0..i] → target[0..j]
Wave N output  = optimal understanding given all waves 0..N-1
```

Neither system looks backward. Both build forward from solved subproblems.

### Memoization = Context Quarantine

In the DP matrix, each cell stores a single integer — the minimum edit count. Not the sequence of edits that produced it. The full history is discarded; only the optimal result is retained.

In rune, each wave produces verbose output — file reads, tool calls, reasoning chains. But only a **2-3 sentence summary** crosses the wave boundary. The full agent output is quarantined in the sub-agent's context window. The main orchestrator carries forward the minimum viable understanding — exactly like the DP cell carrying forward the minimum viable distance.

This is not a limitation. It is the design. Carrying full context forward would be like storing the entire edit sequence in every DP cell — it would bloat memory without improving the result.

### The Critical Path = The Matrix Diagonal

In Levenshtein, the diagonal of the matrix represents substitutions — the cheapest operations when characters match. The diagonal is the shortest path through the matrix when source and target are similar.

In rune, the **critical path** is the longest chain of dependent tasks — the irreducible sequential core that parallelism cannot compress. If Wave 2 depends on Wave 1 which depends on Wave 0, that chain is rune's diagonal: the minimum number of sequential steps regardless of how many parallel tasks fill each wave.

```
Benefit = total_tasks / critical_path_length
```

A Levenshtein distance of 3 on strings of length 7 means most characters already match. A critical path of 4 in a DAG of 7 tasks means most tasks can run in parallel. Both measure how much of the work is inherently sequential.

### Edit Distance as a Knowledge Metric

Before Wave 0, the system knows nothing about the task. The user's desired outcome is the target string. Each wave reduces the edit distance between current understanding and target understanding.

```
Before dispatch:   edit_distance(knowledge, answer) = N
After Wave 0:      edit_distance(knowledge, answer) = N - k₀
After Wave 1:      edit_distance(knowledge, answer) = N - k₀ - k₁
...
After Wave M:      edit_distance(knowledge, answer) = 0
```

The DAG plan is rune computing: **what is the minimum number of transformation waves to get from ignorance to answer?** The safety checks (no cycles, no orphans, no file conflicts) are the equivalent of validating that the DP recurrence is well-formed — that each cell depends only on previously computed cells, never on itself.

---

## Where the Analogy Breaks

Levenshtein optimizes for the **minimum number of edits**. It does not care about parallelism — it processes the matrix cell by cell, left to right, top to bottom.

rune optimizes for **maximum parallelism within the minimum waves**. It is not just "how few operations" but "how many can execute simultaneously." This is edit distance with a **concurrency dimension** — a concept that does not exist in the classical algorithm.

Levenshtein also works on a fixed alphabet. rune's "characters" are arbitrary agent capabilities — a Go developer, a security engineer, a judge — each with different computational properties. The edit operations are not interchangeable the way insert/delete/substitute are in string distance.

Finally, Levenshtein is exact. rune is heuristic. The DP matrix guarantees the optimal edit distance. rune's wave computation guarantees topological correctness but not that the agents will produce optimal output. The Judge exists precisely because the transformation is probabilistic, not deterministic.

---

## Why This Matters

This is not an academic analogy. It is the design principle.

**Context management is state transformation.** Every LLM interaction is a transformation of the context window from one state to another. The question is always: what is the minimum number of well-chosen transformations to reach the target state? rune answers this with dependency graphs and wave-based dispatch. Levenshtein answers it with dynamic programming. The principle is the same.

**Parallelism is the constraint, not the goal.** Levenshtein does not try to parallelize — it accepts sequential processing. rune recognizes that some transformations are independent and exploits that structure. The DAG is the data structure that captures which operations can overlap. Without it, you are processing the DP matrix one cell at a time when entire rows could compute simultaneously.

**Summaries are memoization.** The 2-3 sentence context handoff between waves is the most important design decision in rune. It is not a lossy compression hack — it is optimal substructure preservation. Carry forward the answer, not the work that produced it.

---

*The wisest of all shared his knowledge through runes — transforming understanding one wave at a time, never more operations than necessary, never fewer than sufficient.*
