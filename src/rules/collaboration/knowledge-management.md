# Knowledge Management

> How to maintain, audit, and evolve the rule inventory.
> Covers rule lifecycle, quality criteria, size guidelines, staleness detection, gap analysis, and metrics.
> Theoretical grounding: GRAI framework (Bohm & Durst, 2025, *VINE Journal of Information and Knowledge Management Systems*, Vol. 56, No. 1). [DOI: 10.1108/VJIKMS-10-2024-0357](https://doi.org/10.1108/VJIKMS-10-2024-0357)
> Companion to `rules/toolkit-operations.md` which covers creation/deployment mechanics.

---

## Knowledge Creation Model

rune's knowledge lifecycle is grounded in the SECI model (Nonaka & Takeuchi, 1995) extended with a machine dimension for AI agents. The four phases — Socialization, Externalization, Combination, Internalization — map directly to how knowledge flows through `src/knowledge/` → `src/rules/` → `profiles.yaml` → agent context.

[Read the deep dive →](../../docs/the-knowledge-toolkit.md)

---

## Rule Lifecycle

Every rule progresses through these stages. No rule should exist without an explicit lifecycle status.

```
DRAFT → ACTIVE → REVIEW → (UPDATE | ARCHIVE | DELETE)
                    ↑____________________________|
```

| Stage | Definition | Action |
|---|---|---|
| **Draft** | New rule, not yet deployed to any profile | Author creates, gets review, registers in profiles.yaml |
| **Active** | Deployed in at least one profile, actively consumed by agents | Normal operation. Periodically reviewed. |
| **Review** | Triggered by staleness check, quality audit, or user feedback | Knowledge Manager evaluates: update, split, merge, archive, or delete |
| **Update** | Content revised, structure preserved | Edit in place, redeploy |
| **Archive** | No longer actively needed but may have future value | Move to `src/rules/_archived/`, remove from profiles.yaml |
| **Delete** | Confirmed redundant, incorrect, or permanently superseded | Delete file, remove from profiles.yaml |

### Review Triggers

A rule enters the Review stage when any of these occur:

- **Age**: not modified in 6+ months and contains version-specific content (API versions, tool versions, pricing)
- **Size**: exceeds 800 lines (see Size Guidelines below)
- **Coverage**: exists in `src/rules/` but is not referenced by any profile
- **Duplication**: overlaps significantly (>30% content) with another rule
- **Feedback**: an agent or user reports the rule is incomplete, incorrect, or confusing
- **Source update**: the underlying source material (paper, documentation, product) has been updated

---

## Pre-Creation Checklist

Before creating a new rule, verify these conditions. Skipping this step leads to duplication and bloat.

| Check | How | Fail Action |
|---|---|---|
| **Goal defined** | Can you state in one sentence what agent behavior this rule changes? | Do not create — vague rules waste context |
| **No duplicate exists** | `grep -rl "keyword" src/rules/` for key terms | Extend the existing rule instead of creating a new one |
| **Clear audience** | Which profiles will deploy this rule? | If no profile needs it, do not create it |
| **Source material available** | Is there a concrete source (paper, docs, article) to base the rule on? | Defer until source is identified — unsourced rules degrade over time |
| **Right granularity** | Does this warrant its own file, or is it a section in an existing rule? | Add as a section if <50 lines of content |

---

## Quality Criteria

A good rule satisfies all five criteria. A rule that fails two or more should be flagged for review.

### The Five Criteria

| # | Criterion | Test | Bad Example | Good Example |
|---|---|---|---|---|
| 1 | **Actionable** | Does it tell agents what to do, not just what to know? | "The database supports partitioning" | "Always partition tables >1 GB by date. Set `require_partition_filter = true`." |
| 2 | **Structured** | Tables, checklists, and code blocks over prose paragraphs? | Three paragraphs explaining SCD types | Comparison table with columns: Type, History, Complexity, Use When |
| 3 | **Sourced** | Are claims attributed to a specific source with author, year, publication? | "Studies show value investing works" | "Asness, Moskowitz & Pedersen (2013), Journal of Finance, Vol. 68, No. 3" |
| 4 | **Scoped** | Does it cover one coherent topic without sprawling into adjacent domains? | A "Cloud" rule covering compute, storage, networking, and IAM | Separate rules: `cloud-compute.md`, `cloud-storage.md`, `cloud-iam.md` |
| 5 | **Current** | Is the content accurate as of today? Are version numbers, API endpoints, and pricing correct? | "Use `deprecated_api_v1` resources" (deprecated) | "Use `new_api_v2` resources. The v1 API is deprecated; see migration path." |

### Rule Structure Template

Every rule should follow this structure:

```markdown
# Topic Title

> One-line description of what this rule covers.
> Source attribution: author, title, year, publication.
> Connection to workflows: how this relates to agent tasks.

---

## Section 1: Core Content

Tables, code blocks, checklists.

---

## Section 2: Practical Application

How to use this knowledge in analysis/engineering/operations.

---

## Cross-References

- See `rules/related-topic.md` for adjacent content
```

Required elements:
- **Header block** (`>` quoted lines): description, source, connection to workflows
- **Horizontal rules** (`---`): separate major sections
- **Cross-references**: link to related rules at the bottom

---

## Size Guidelines

Rule size directly impacts agent context consumption. Every line loaded into context displaces space for reasoning.

| Size (lines) | Classification | Action |
|---|---|---|
| < 50 | **Minimal** | Consider whether this should be merged into a related rule |
| 50-300 | **Lean** | Ideal range. Focused, easy to consume. |
| 300-500 | **Standard** | Acceptable for comprehensive reference topics |
| 500-800 | **Heavy** | Review for split opportunities. Acceptable only for genuinely indivisible topics (full methodology references, multi-segment market analyses) |
| > 800 | **Bloated** | Must be split or trimmed. No single rule should exceed 800 lines except with explicit justification. |

### When to Split

Split a rule when:
- It covers multiple distinct sub-topics that different profiles need independently (e.g., a "Cloud" rule should split into per-service rules)
- Different sections have different staleness rates (e.g., pricing changes quarterly, architecture changes annually)
- Different agents need different sections (e.g., the API section vs. the CLI section)
- The rule exceeds 800 lines

### When to Merge

Merge rules when:
- Two rules cover the same topic from slightly different angles (redundancy)
- A rule is under 50 lines and its topic is a natural sub-section of another rule
- Two rules are always deployed together in every profile that uses either

### Split Strategy

When splitting, preserve cross-references:

1. Identify natural boundaries (sub-topics, segments, layers)
2. Create new files with clear, specific names
3. Add cross-references in each new file pointing to the others
4. Update profiles.yaml -- profiles that had the original rule should get all splits
5. Update agent header blocks if they referenced the original rule

---

## Staleness Detection

### Automated Checks

Run these checks periodically (monthly recommended) to identify stale content.

**1. Last-modified date audit:**

```bash
# Rules not modified in 6+ months
find src/rules -name "*.md" -mtime +180 -exec ls -la {} \;
```

**2. Orphan rules (not in any profile):**

```bash
# List all rule filenames (without extension)
find src/rules -name "*.md" -exec basename {} .md \; | sort > /tmp/all_rules.txt

# List all rules referenced in profiles.yaml
grep -oP '^\s+- \K\S+' profiles.yaml | sort -u > /tmp/profiled_rules.txt

# Find orphans
comm -23 /tmp/all_rules.txt /tmp/profiled_rules.txt
```

**3. Size distribution:**

```bash
# Line counts sorted descending
find src/rules -name "*.md" -exec wc -l {} + | sort -rn | head -20
```

**4. Category balance:**

```bash
# Rules per category
for dir in src/rules/*/; do
    echo "$(basename $dir): $(find $dir -name '*.md' | wc -l) rules, $(find $dir -name '*.md' -exec cat {} + | wc -l) total lines"
done
```

### Manual Review Checklist

For each rule flagged by automated checks:

- [ ] **Version references**: Are API versions, tool versions, or SDK versions still current?
- [ ] **Pricing**: Has pricing changed since the rule was written?
- [ ] **Deprecated features**: Does the rule reference deprecated services, APIs, or patterns?
- [ ] **Broken links**: Do cross-references point to rules that still exist?
- [ ] **Accuracy**: Has the underlying source material been updated or superseded?
- [ ] **Relevance**: Is this topic still actively used by the team?

---

## Gap Analysis

Gaps are topics that agents need but no rule covers. Identify them through:

### 1. Agent Header Block Audit

Check each agent's `>` header block for references to rules that do not exist:

```bash
# Extract rule references from agent files
grep -rh 'rules/' src/agents/ | grep -oP 'rules/[a-z0-9-]+\.md' | sort -u > /tmp/agent_refs.txt

# Check which referenced rules actually exist
while read ref; do
    file="src/$ref"
    if [ ! -f "$file" ]; then
        echo "MISSING: $ref"
    fi
done < /tmp/agent_refs.txt
```

### 2. Profile Coverage Matrix

For each profile, check whether its rules cover the agent's described responsibilities:

| Profile | Agent Responsibilities | Rules Covering Them | Gaps |
|---|---|---|---|
| `developer` | Code generation, debugging, testing | language-conventions, testing-patterns, api-design | Performance best practices? |
| `devops` | CI/CD, deployments, infrastructure | ci-cd-pipelines, deployment-patterns, monitoring | Disaster recovery? |
| ... | ... | ... | ... |

### 3. Conversation Mining

When agents are asked questions they cannot answer from existing rules, that topic is a gap candidate. After each research session, ask:

- Did I need to look up information that should have been in a rule?
- Did I generate content that could benefit other agents?
- Did I find an error in an existing rule?

### 4. Source Material Tracking

Maintain a list of source materials that have been ingested vs. materials that are known but not yet ingested. Each entry should note:

- Source title and author
- Date discovered
- Priority (high/medium/low)
- Which agent(s) would benefit
- Status (ingested / pending / rejected)

---

## Metrics

Track these metrics to measure knowledge base health over time.

### Inventory Metrics

| Metric | How to Measure | Target |
|---|---|---|
| Total rules | `find src/rules -name "*.md" \| wc -l` | -- (track trend) |
| Total lines | `find src/rules -name "*.md" -exec cat {} + \| wc -l` | -- (track trend) |
| Average rule size | Total lines / total rules | 150-400 lines |
| Rules > 800 lines | Count of bloated rules | 0 |
| Rules < 50 lines | Count of minimal rules | Minimize |
| Orphan rules | Rules not in any profile | 0 |

### Coverage Metrics

| Metric | How to Measure | Target |
|---|---|---|
| Profile rule count | Count rules per profile (including global) | 10-25 per profile |
| Rules per category | Count per `src/rules/{category}/` | Balanced, no empty categories |
| Agent-rule alignment | Cross-check agent headers vs. profile rules | All agent references resolve |

### Health Metrics

| Metric | How to Measure | Target |
|---|---|---|
| Stale rules (>6 months unmodified) | `find -mtime +180` | < 20% of inventory |
| Rules with no source citation | Manual audit of header blocks | 0 (all rules must cite sources) |
| Duplicate content | Manual review or diff-based analysis | 0 significant overlaps |

---

## Discoverability

Rules are only useful if agents and users can find them. Optimize for discoverability:

### Rule Titles
- The `# Title` heading must describe the topic clearly enough to assess relevance without reading the body
- Bad: `# Reference` — too vague. Good: `# Database CLI Reference` — immediately scoped

### Header Block
- The `>` quoted lines at the top serve as the rule's abstract — they are the first thing read during search
- Include: what it covers, source attribution, which workflows it connects to
- An agent scanning headers should be able to decide in <5 seconds whether this rule is relevant

### Cross-References
- Every rule must end with a `## Cross-References` section linking to related rules
- This creates a navigable graph — agents can follow references to find adjacent knowledge
- When creating a new rule, add back-references in the related rules pointing to the new one

### Profile as Discovery Mechanism
- Profiles are the primary way agents receive relevant rules — a rule not in a profile is invisible
- When a rule applies to multiple workstreams, add it to all relevant profiles rather than relying on agents to find it

---

## Anti-Patterns

Specific mistakes that degrade knowledge base quality. The Knowledge Manager should flag these during audits.

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **Information overload** | Rule >800 lines trying to cover everything about a topic | Split into focused sub-rules |
| **Stale encyclopedia** | Rule not updated in 12+ months with version-specific content | Review and update, or archive |
| **Orphan rule** | Exists in `src/rules/` but no profile deploys it | Add to relevant profile or archive |
| **Duplicate coverage** | Two rules explain the same concept differently | Merge into one authoritative source |
| **Prose over structure** | Long paragraphs instead of tables, checklists, code blocks | Restructure — agents parse structure faster than prose |
| **Missing attribution** | Claims without source — degrades trust and makes updates impossible | Add source with author, year, publication |
| **Just-in-case inclusion** | Rule added to a profile "because it might be useful" | Remove — every rule consumes context tokens |
| **No cross-references** | Rule exists in isolation, not linked to related rules | Add `## Cross-References` section |

---

## Naming and Organization Conventions

### File Names

- **Lowercase kebab-case**: `api-design-patterns.md`, `cloud-compute-services.md`
- **Prefix by domain**: `aws-*` for AWS services, `api-*` for API topics
- **No abbreviations** unless universally understood: `api` (yes), `k8s` (yes), `db` (no -- use `database`)
- **Descriptive**: the filename should tell you what the rule covers without opening it
- **Unique repo-wide**: the deploy script resolves by recursive search -- duplicates cause ambiguity

### Category Assignment

| Category | Belongs Here |
|---|---|
| `collaboration` | Cross-cutting: git, design patterns, operational constraints, toolkit operations, knowledge management |
| `data` | Data modeling, SQL, data pipelines, data sources, analytics |
| `engineering` | Language-specific conventions, API design, architecture patterns |
| `infra` | Cloud services, infrastructure as code, CI/CD infrastructure, observability |
| `python` | Python-specific: asyncio, uv, pandas, CLI development |
| `regulatory` | Compliance frameworks, security policies, governance |

When a rule spans two categories, place it in the category most aligned with its primary consumers. Add cross-references to related rules in the other category.

### Profile Assignment

- **Global rules** (`global_rules` in profiles.yaml): only rules that EVERY agent needs regardless of workstream (operational constraints, git conventions, toolkit operations)
- **Profile-specific rules**: only rules the profile's target workflow actually consumes
- **Never add a rule to a profile "just in case"** -- every rule consumes context tokens

---

## Archive Process

When a rule is no longer needed but may have future value:

1. Create `src/rules/_archived/` directory if it does not exist
2. Move the rule: `mv src/rules/{category}/{rule}.md src/rules/_archived/{rule}.md`
3. Remove from profiles.yaml
4. Remove references from agent header blocks
5. Add a one-line note at the top of the archived file: `> ARCHIVED {date}: {reason}`
6. Deploy: `make use-profile PROFILE={active_profile}`

Archived rules are not deployed but remain in the repository for reference. They can be restored by reversing the process.

---

## Cross-References

- See `rules/toolkit-operations.md` for rule creation, deployment, and profile management mechanics
