Phase: Plan

# Architectural Decision Records (ADRs)

One decision per record. 1-2 pages max. Immutable after acceptance unless
overwritten by HITL. Otherwise supersede, never silently edit. Store in source
control next to code, never a wiki.

## When to Write

Write ADR: choosing frameworks/libraries/tools, API contracts/data formats, deployment/infra patterns, security/compliance choices, competing architectural patterns. Write RFC first if decision spans multiple teams/repos. Skip ADR for routine reversible choices or existing policy.

## Agent Requirements

**ADR work requires an opus subagent** (1M context) for writing, reviewing, and superseding. Sonnet acceptable only for simple compliance checks. Set `model: "opus"` when dispatching. Multiple ADR tasks may run as parallel opus subagents.

## ADR vs RFC vs Design Doc

| Doc | Purpose | Timing | Mutability |
|---|---|---|---|
| RFC | Solicit feedback | Before decision | Mutable during discussion |
| ADR | Record one decision + rationale | At/after decision | Immutable after acceptance |
| Design Doc | Implementation specification | Before/during impl | Living document |

Flow: RFC (debate) → ADR (record) → Design Doc (detail). Small decisions skip RFC.

## Status Lifecycle

`Proposed → Accepted → Superseded by ADR-NNNN` or `→ Deprecated` (no replacement). `Proposed → Rejected` is also valid.

| Status | Can Modify Content? |
|---|---|
| Proposed | Yes |
| Accepted | No — immutable |
| Rejected | No — immutable |
| Deprecated | Add deprecation note only |
| Superseded | Add "superseded by" link only |

**To supersede:** write new ADR with next sequential number, reference old ADR
in Context, update old ADR metadata status only, and record the replacement.
ADRs require review before acceptance; the human is the sole authority for
status changes.

## Directory Structure and Naming

**Platform-wide:** `docs/decisions/{infrastructure,data,api,security,governance}/`
**Per-service:** `{repo}/docs/decisions/`
**Plans:** `docs/plans/` (mutable, tracked)
**Ephemeral prep notes:** `.rune/adr-prep/`

Use `decisions`, not `adrs`, in tracked paths.

**Naming:** 4-digit zero-padded + kebab-case: `0001-use-react-for-frontend.md`. Numbers never reused. Per-repo for service-scoped decisions, centralized for cross-cutting, or hybrid.

## ADR Readiness — When an Architectural Decision Is Ready to Be Made

### The Five ADMM Logical Steps

Architectural Decision Management Method (ADMM) describes five logical steps. They are not strictly sequential — going back and forth between steps is normal and expected.

| Step | What Happens |
|---|---|
| 1. Identification | Surface the design issue and the options that could address it |
| 2. Criteria and analysis | Evaluate options against decision drivers; document pros/cons |
| 3. Decision making | Choose an option, develop rationale, reach stakeholder agreement |
| 4. Capturing | Write the ADR — what was decided, why, and what the consequences are |
| 5. Enforcement | Implement the decision and review the outcome over time |

### Definition of Ready — the START Checklist

An architectural decision is ready to be made when ALL five criteria are satisfied. This is the DoR gate — do not write the ADR stub until START is green.

| Letter | Criterion | Check |
|---|---|---|
| **S** | **Stakeholders are known** — decision makers, consulted parties, and people affected by the outcome (RACI) | Are all roles identified? |
| **T** | **Time has come** — the Most Responsible Moment has arrived; the decision is both important and urgent now | Is this the right moment — not too early, not too late? |
| **A** | **Alternatives exist and are understood** — at least two options defined, with pros/cons known or plannable | Are ≥2 options defined with consequences understood? |
| **R** | **Requirements/criteria and context are known** — decision drivers have been analysed and documented | Are the decision drivers clear? |
| **T** | **Template chosen and log record created** — ADR template selected and stub pre-populated, ready to fill in as the decision is made | Is the ADR stub ready? |

```
DoR checklist (copy into your ADR prep notes):
* [ ] Stakeholders are known (decision makers and those affected)
* [ ] Time (Most Responsible Moment) has come
* [ ] Alternatives/options exist and are understood (at least two)
* [ ] Requirements/criteria and context/problem are known
* [ ] Template chosen and log record created
```

### Timing — The Most Responsible Moment

"Don't decide too early — this harms flexibility. Don't decide too late — this wastes the window to shape the outcome."

The Most Responsible Moment (MRM) is the latest point at which deferring costs more than deciding. Before the MRM: keep options open. After the MRM: the decision is overdue.

Procrastinating beyond the MRM — especially on significant decisions — often signals uncertainty or avoidance, not good judgment.

### When to Make a Decision Early ("Big ADs")

Seven signals that an architectural decision should be made early rather than deferred:

| Signal | Why it justifies early decision |
|---|---|
| High architectural significance | High significance score or H/H position in utility tree — the decision shapes everything downstream |
| High cost or tough consequences | Software licences, cloud costs, training investment, or staff impact; late changes are expensive |
| Long time to execute | Spikes, PoCs, procurement, or recruiting needed — start the clock early |
| Many or unclear outgoing dependencies | The decision triggers other decisions; deferring creates a cascade of blocked work |
| Long time to make | Many stakeholders, expected goal conflicts, or outcomes that are hard to revise once made |
| High abstraction requiring refinement | Architectural style selection triggers follow-on technology and product decisions |
| Unusual problem or solution space | Outside the team's comfort zone; more orientation and learning is needed before deciding safely |

If any of these signals apply, treat it as a Big AD and prioritise reaching the DoR gate early in the project or sprint.

### Definition of Done (reference)

An AD is done (ready to mark `accepted`) when:

- Evidence that the chosen option will work is documented
- Criteria used for option selection are documented
- Agreement among stakeholders is reached
- AD outcome and rationale are captured in the ADR
- A realization or review plan is in place

## ADR Decision-Making Fallacies

### The Seven Fallacies

Scan this table when evaluating an ADR draft or framing a design question. Each fallacy is a reasoning error that produces a bad decision regardless of how well the ADR is formatted.

| # | Name | Symptom to detect | Countermeasure |
|---|---|---|---|
| 1 | **Blind flight** | No NFRs stated; quality goals are vague ("it should be fast", "it should scale"); context from prior projects assumed without comparison | Elicit SMART NFRs before evaluating options. Make context explicit. Compare with previous projects before reusing solutions. |
| 2 | **Following the crowd** | Justification is "X uses this" or "it's the industry standard"; no requirement compatibility check | Apply explicit criteria (the ADR's Decision Drivers). Trends are bad scouts — verify requirement fit independently. |
| 3 | **Anecdotal evidence** | Single blog post, one team's war story, or tribal knowledge cited as conclusive evidence; confidence level not stated | Use SMART NFRs as selection criteria. State confidence level explicitly. Flag gut-feel arguments as such — they are acceptable but must be labelled. |
| 4 | **Blending whole and part** | One bad pattern → entire pattern language rejected; one fitting component → entire architectural style adopted; system-wide and local arguments mixed in one ADR | Be explicit about scope. It is valid to adopt a style partially. Do not mix system-wide and local arguments in one ADR. |
| 5 | **Abstraction aversion** | Pattern choice, technology choice, and product/vendor selection collapsed into one ADR; no separation of "what kind of problem is this?" from "what tool solves it?" | Separate abstract/conceptual arguments from concrete/technological ones. Use related ADRs: one for the pattern, one for the technology, one for the product. |
| 6 | **Golden hammer / silver bullet** | Only one option considered; "we always use X"; no alternatives explored; option presented as universally applicable | Always provide ≥2 genuine alternatives with pros/cons. Stay open to options outside the current toolbox. Flag Résumé-Driven Development explicitly. |
| 7 | **Time dimension deemed irrelevant** | Old benchmarks or evaluations cited without checking currency; no review date set; lifecycle (disposable vs. durable) not stated | Make expected lifecycle explicit. Set a review-by date for significant ADs. Re-run technical evaluations (benchmarks, security reviews) before citing them as current arguments. |

**Bonus — AI über-confidence:** Blind faith in AI-generated design advice without quality assurance. If fallacies are baked into the prompt, the AI will reproduce them confidently. All seven fallacies above apply equally to AI-generated ADR content — treat it as a first draft requiring human review.

### Motivating Example

> "We will build our online shop as a set of microservices because our cloud provider does that successfully in its infrastructure. They also provide a reference architecture for this variant of SOA, a de-facto standard for modern enterprise applications."

This single sentence contains three fallacies:

| Clause | Fallacy |
|---|---|
| "our cloud provider does that successfully" | **#2 — Following the crowd.** Their context is unknown; no requirement compatibility check. |
| "a reference architecture for this variant" | **#3 — Anecdotal evidence.** A reference architecture is one team's experience, not a universal proof. |
| No separation of "microservices (style)" from "SOA (category)" from specific tooling | **#5 — Abstraction aversion.** Pattern, architectural style, and technology are collapsed into one claim. |

A corrected framing would: (1) state the specific quality goals that microservices must satisfy for this shop, (2) compare against at least one alternative decomposition, and (3) write separate ADRs for the decomposition style and the enabling technology choices.

### Review Checklist for the Technical Writer

When reviewing an ADR draft, scan the Considered Options and Decision Outcome sections for these signals:

- [ ] Is at least one NFR (non-functional requirement) cited as a decision driver? If not, flag **#1 Blind flight**.
- [ ] Does any justification appeal only to popularity, industry trend, or a named company's practice? Flag **#2 Following the crowd**.
- [ ] Is confidence level stated for any evidence cited? If a blog post or single case study is the only source, flag **#3 Anecdotal evidence**.
- [ ] Does the ADR mix system-wide and local-scope arguments in the same section? Flag **#4 Blending whole and part** and propose a scope split.
- [ ] Are pattern selection and technology/product selection conflated? Flag **#5 Abstraction aversion** and suggest separate related ADRs.
- [ ] Does the Considered Options section list only one real option (with one obviously unworkable straw man)? Flag **#6 Golden hammer** — request at least one genuine alternative.
- [ ] Are any benchmarks, case studies, or evaluations cited without a date or recency check? Flag **#7 Time dimension** and request a currency check before acceptance.

### Planner Guidance

When framing a design question before writing a plan or ADR:

- **Before proposing options**: name the problem class (e.g., "this is a data consistency problem", "this is a read-scaling problem"). Skipping this step is Fallacy #5.
- **When options feel obvious**: that is a signal to look harder, not to skip the search. Obvious options are a symptom of Fallacy #6.
- **When citing evidence**: note its source type (benchmark, case study, tribal knowledge, first-principles reasoning) and state your confidence level explicitly.
- **When proposing a reuse of a previous decision**: check whether the context still matches. Changed NFRs, scale, or team size may invalidate a previously sound decision. This is Fallacy #7.
- **When AI-assisted**: explicitly instruct the model not to fabricate references or benchmarks, and treat any cited evidence as unverified until checked.

### Anti-Patterns

| Anti-Pattern | Failure |
|---|---|
| Fairy Tale | Only benefits, no trade-offs |
| Sales Pitch | Marketing language, no evidence |
| Free Lunch Coupon | Hides downsides |
| Dummy Alternative | Unworkable options to favor preferred choice |
| Sprint | One option, short-term only |
| Tunnel Vision | Ignores stakeholders beyond immediate team |
| Mega-ADR | Should be a design doc |
| Blueprint in Disguise | Reads like a cookbook, not a decision journal |

**Quality checklist:** problem stated in 2-3 sentences, ≥2 genuine alternatives, both positive AND negative consequences documented, under 2 pages, active voice ("We will...").

## ADRs and AI Agents

ADRs answer "why" — information code cannot provide. "Considered Options" prevents agents from recommending rejected alternatives. Structured format constrains solution space, reducing hallucination.

**AI-drafted ADRs:** provide brief decision statement → LLM expands to MADR → team reviews and argues → use Reviewer agent to critique before human review. Mitigations: LLMs hallucinate references — fact-check every link, instruct "do not fabricate features or references", treat output as first draft only.

**Include ADRs in `llms.txt`** for AI discoverability.

## MADR 4.0 Template

Copy this template to start a new ADR.

```markdown
---
# These are optional metadata elements. Feel free to remove any of them.
description: "MADR 4.0 template for recording architectural decisions — context, options, outcome, and consequences."
status: "{proposed | rejected | accepted | deprecated | … | superseded by ADR-0123}"
date: {YYYY-MM-DD when the decision was last updated}
decision-makers: {list everyone involved in the decision}
consulted: {list everyone whose opinions are sought (typically subject-matter experts); and with whom there is a two-way communication}
informed: {list everyone who is kept up-to-date on progress; and with whom there is a one-way communication}
---

# {short title, representative of solved problem and found solution}

## Context and Problem Statement

{Describe the context and problem statement, e.g., in free form using two to three sentences or in the form of an illustrative story. You may want to articulate the problem in form of a question. Consider adding links to collaboration boards or issue management systems. Make the scope of the decision explicit, for instance, by calling out or pointing at structural architecture elements (components, connectors, ...)}

<!-- This is an optional element. Feel free to remove. -->
## Decision Drivers

* {decision driver 1, for instance, a desired software quality, faced concern, constraint or force}
* {decision driver 2}
* … <!-- numbers of drivers can vary -->

## Considered Options

* {title of option 1}
* {title of option 2}
* {title of option 3}
* … <!-- numbers of options can vary -->

## Decision Outcome

Chosen option: "{title of option 1}", because {justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force {force} | … | comes out best (see below)}.

<!-- This is an optional element. Feel free to remove. -->
### Consequences

* Good, because {positive consequence, e.g., improvement of one or more desired qualities, …}
* Bad, because {negative consequence, e.g., compromising one or more desired qualities, …}
* … <!-- numbers of consequences can vary -->

<!-- This is an optional element. Feel free to remove. -->
### Confirmation

{Describe how the implementation / compliance of the ADR can/will be confirmed. Is there any automated or manual fitness function? If so, list it and explain how it is applied. Is the chosen design and its implementation in line with the decision? E.g., a design/code review or a test with a library such as ArchUnit can help validate this. Note that although we classify this element as optional, it is included in many ADRs.}

<!-- This is an optional element. Feel free to remove. -->
## Pros and Cons of the Options

### {title of option 1}

<!-- This is an optional element. Feel free to remove. -->
{example | description | pointer to more information | …}

* Good, because {argument a}
* Good, because {argument b}
<!-- use "neutral" if the given argument weights neither for good nor bad -->
* Neutral, because {argument c}
* Bad, because {argument d}
* … <!-- numbers of pros and cons can vary -->

### {title of other option}

{example | description | pointer to more information | …}

* Good, because {argument a}
* Neutral, because {argument b}
* Bad, because {argument c}
* …

<!-- This is an optional element. Feel free to remove. -->
## More Information

{You might want to provide additional evidence/confidence for the decision outcome here and/or document the team agreement on the decision and/or define when/how this decision the decision should be realized and if/when it should be re-visited. Links to other decisions and resources might appear here as well.}
```

### Y-Statement (inline/quick capture for commits/PRs)

> "In the context of **{use case}**, facing **{concern}**, we decided for **{option}** and neglected **{other options}**, to achieve **{qualities}**, accepting **{downside}**, because **{rationale}**."
