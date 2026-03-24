# The Knowledge Creation Cycle

> How rune turns scattered expertise into structured, deployable agent knowledge — grounded in organizational knowledge theory.

---

## The Problem

Engineering teams accumulate knowledge in conversations, code reviews, incident postmortems, and tribal memory. Most of it never becomes reusable. An engineer learns something on Tuesday, forgets the details by Friday, and the next person rediscovers it from scratch.

AI coding agents make this worse. They start every session with zero project knowledge unless you explicitly load it. The context window is powerful but empty by default.

rune's knowledge lifecycle — Feed, Shape, Grow — exists to solve this. The theory behind it explains why it works.

---

## The SECI Model (Nonaka & Takeuchi, 1995)

The foundational model of organizational knowledge creation describes four phases in a cycle:

| Phase               | Transformation      | What Happens                                                                                                                        |
| ------------------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Socialization**   | tacit → tacit       | Knowledge surfaces in conversation — one person's experience transfers to another through dialogue, observation, or shared practice |
| **Externalization** | tacit → explicit    | Unstructured knowledge is codified into documents, rules, checklists — something that can be read independently                     |
| **Combination**     | explicit → explicit | Existing documents are audited, merged, split, cross-referenced — structured knowledge is refined and organized                     |
| **Internalization** | explicit → tacit    | Documents are absorbed by practitioners (or agents) and shape their behavior — knowledge becomes instinct                           |

The cycle repeats. Each rotation compounds the organization's knowledge base.

## How rune Implements It

| SECI Phase          | rune Mechanism                                                                                                                                  | Who Does It             |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| **Socialization**   | Conversations between user and agents surface gaps — topics where agents lack knowledge reveal what rules are missing                           | User + any agent        |
| **Externalization** | Raw material lands in `src/knowledge/`. The Knowledge Manager distills it into structured rules in `src/rules/`                                 | Knowledge Manager agent |
| **Combination**     | The Knowledge Manager audits rule quality, detects staleness, finds gaps, splits oversized rules, merges duplicates, maintains cross-references | Knowledge Manager agent |
| **Internalization** | `make use-profile` loads rules into agent context. The rules shape agent behavior — they become the agent's working memory                      | Deploy system           |

The `src/knowledge/` inbox is the bridge between socialization and externalization. Raw PDFs, research summaries, extracted documentation — anything that is not yet structured for agent consumption. The Knowledge Manager reads the inbox and produces focused, actionable rules. Never skip the inbox by dumping raw content directly into rules.

---

## The Machine Dimension

Cerchione, Liccardo & Passaro (2026, *Journal of Innovation & Knowledge*, Vol. 11) extend the SECI model with a critical insight: **AI agents are not just tools that process knowledge — they are epistemic actors that generate it.**

This has two implications for rune:

### DIKW Inversion

Humans create knowledge bottom-up: data → information → knowledge → wisdom. We observe facts, organize them into patterns, and eventually develop judgment.

AI agents work top-down. They are trained on structured knowledge (rules) and produce novel outputs — analysis, code, recommendations — that function as new data. When an agent synthesizes a report from rules and source material, it is creating **artificial knowledge**: structured output that did not exist before.

This output should be evaluated for re-ingestion as a new rule when it represents reusable insight. The cycle is not linear — it spirals. Agent output feeds back into the knowledge base that shapes future agent behavior.

### Profile Selection as Cognitive Shaping

An agent's loaded rules function as its "tacit knowledge" — shaping behavior without being explicitly articulated in outputs. A platform engineer agent loaded with Terraform conventions writes different code than the same agent loaded with Kubernetes conventions.

This means **profile selection is the primary lever for shaping agent cognition**. Loading the wrong rules (or too many) is equivalent to giving a human the wrong training. Profiles are not just organizational convenience — they are the mechanism by which you control what your team knows.

---

## Measuring the Cycle

Each phase can degrade. When it does, the symptom is predictable:

| Gap                     | Symptom                                                               | Fix                                                                                       |
| ----------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **Socialization gap**   | Agents repeatedly ask users for information that should be in a rule  | Run gap analysis — the missing knowledge exists in someone's head but not in `src/rules/` |
| **Externalization gap** | Source materials are known but not yet ingested                       | Check `src/knowledge/` inbox — raw material is waiting for distillation                   |
| **Combination gap**     | Rules exist but are poorly cross-referenced, duplicated, or bloated   | Run a Knowledge Manager audit — split, merge, and clean                                   |
| **Internalization gap** | Rules exist but agents do not use them                                | Check profile coverage — the rule may not be deployed to the right profiles               |
| **Generation gap**      | Agents produce valuable outputs that are never captured back as rules | Set up a feedback loop — review agent outputs for reusable insights                       |

The generation gap is unique to AI-augmented teams. Traditional SECI does not account for it because traditional organizations do not have epistemic actors that produce structured output at scale. rune does.

---

## Why This Matters

Most AI agent frameworks focus on execution — how to dispatch tasks, how to call tools, how to chain prompts. rune focuses on **what the agents know** and **how that knowledge evolves**.

Execution without knowledge is automation. Knowledge without execution is a wiki. rune combines both: structured knowledge that shapes agent behavior, refined by the agents themselves, deployed through profiles that match knowledge to role.

The SECI cycle is why "Feed, Shape, Grow" is not a marketing tagline — it is the operational loop that makes the system compound over time.

---

## Sources

- Nonaka, I. & Takeuchi, H. (1995). *The Knowledge-Creating Company*. Oxford University Press.
- Böhm, S. & Durst, S. (2025). "GRAI Framework for AI-Augmented Knowledge Creation." *VINE Journal of Information and Knowledge Management Systems*, Vol. 56, No. 1.
- Cerchione, R., Liccardo, A. & Passaro, R. (2026). "The Machine Dimension in Knowledge Creation." *Journal of Innovation & Knowledge*, Vol. 11.

---

*The wisest of all shared his knowledge through runes — not by hoarding it, but by structuring it so others could absorb and build upon it.*
