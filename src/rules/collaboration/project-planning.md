# Project Planning Frameworks

> Actionable planning frameworks adapted from PMBOK Guide 7th Edition (PMI, 2021).
> Source: Project Management Institute. The Standard for Project Management and A Guide to the Project Management Body of Knowledge, 7th ed. Newtown Square, PA: PMI, 2021.
> Use when the Planner agent creates implementation plans, breaks down complex features, or assesses plan completeness.

---

## 12 Principles of Project Management

Use as a checklist when reviewing plan quality. Every plan should demonstrably address the applicable principles.

| # | Principle | Planning Implication | Check |
|---|---|---|---|
| 1 | **Be a diligent steward** | Plan should respect resource constraints (budget, time, people). Flag overcommitment. | Does the plan acknowledge capacity limits? |
| 2 | **Create a collaborative team environment** | Identify who does what. Clarify authority, accountability, and responsibility for each step. | Are roles and ownership explicit? |
| 3 | **Effectively engage stakeholders** | Identify stakeholders affected by the plan. Include review/approval checkpoints. | Are stakeholder touchpoints built in? |
| 4 | **Focus on value** | Every phase should deliver measurable value. Avoid planning work that doesn't advance outcomes. | Can each phase's value be stated in one sentence? |
| 5 | **Recognize system interactions** | Changes in one component affect others. Map dependencies explicitly. | Are cross-component impacts identified? |
| 6 | **Demonstrate leadership** | The plan should enable decision-making, not defer it. Include decision points. | Are decisions made or deferred? |
| 7 | **Tailor based on context** | Adapt planning depth to the project. Small changes need thin plans; large changes need detailed ones. | Is planning depth proportional to risk and complexity? |
| 8 | **Build quality into processes** | Quality checks at each phase, not just at the end. Include verification steps. | Are quality gates defined per phase? |
| 9 | **Navigate complexity** | Use the complexity taxonomy below to match response strategy to the type of complexity. | Is the dominant complexity type identified? |
| 10 | **Optimize risk responses** | Classify risks by type (threat/opportunity). Match response strategy to risk type. | Are risks classified and responses matched? |
| 11 | **Embrace adaptability** | Build in iteration points. Plans should be living documents, not rigid prescriptions. | Can the plan adapt to new information? |
| 12 | **Enable change** | The plan should move the system toward its desired future state, not just maintain current state. | Does the plan advance toward the target architecture? |

---

## Uncertainty Taxonomy

Not all uncertainty is the same. Identify which type dominates your project and match the response strategy.

| Type | Definition | Response Strategies |
|---|---|---|
| **Ambiguity** | Unclear requirements, multiple interpretations, vague scope | Progressive elaboration, prototyping, experiments, spikes |
| **Complexity** | Many interconnected parts with unpredictable interactions | Decoupling (isolate subsystems), iteration (build incrementally), diverse perspectives, fail-safe design |
| **Volatility** | Rapid, unpredictable changes in environment, requirements, or resources | Alternatives analysis, schedule/cost reserves, flexible architecture |
| **Risk** | Specific uncertain events with known probability and impact | **Threats**: avoid, mitigate, transfer, accept, escalate. **Opportunities**: exploit, enhance, share, accept, escalate |

### Applying to Implementation Plans

When writing the "Risks & Mitigations" section of a plan:

1. **Classify each risk** as ambiguity, complexity, volatility, or risk (specific event)
2. **Select the matching strategy** from the table above
3. **Avoid using "risk" as a catch-all** — a requirement that's unclear is ambiguity (solve with a spike), not a risk (solve with mitigation)

---

## 8 Performance Domains — Plan Completeness Check

Use these as a completeness checklist after drafting a plan. Each domain should be addressed, even if briefly.

| Domain | Question to Ask | If Missing |
|---|---|---|
| **Stakeholders** | Who is affected? Who needs to approve? Who will use the output? | Add stakeholder identification and engagement plan |
| **Team** | Who executes each step? What skills are needed? Are they available? | Add role assignments and capacity check |
| **Development Approach** | Predictive (waterfall), adaptive (agile), or hybrid? What cadence? | Explicitly state the approach and why |
| **Planning** | Is planning depth appropriate? Are estimates provided? | Adjust planning detail to match uncertainty level |
| **Project Work** | How is work tracked? How are changes managed? | Add progress tracking and change management |
| **Delivery** | What is delivered at each phase? How is quality verified? | Add deliverables and acceptance criteria per phase |
| **Measurement** | How do we know the plan is succeeding? What metrics? | Add success criteria with measurable indicators |
| **Uncertainty** | What could go wrong? What opportunities exist? | Add uncertainty assessment using the taxonomy above |

---

## Tailoring Planning Depth

Not every task needs the same level of planning. Match depth to context.

| Signal | Planning Depth | Example |
|---|---|---|
| Small, well-understood change | **Thin** — 1-paragraph summary, no phases | Bug fix, config change, minor refactor |
| Moderate feature, known patterns | **Standard** — phases, steps, risks, testing | New API endpoint, service module, dashboard |
| Large feature, multiple components | **Detailed** — full plan with all 8 domains, stakeholders, decision points | New service, cross-repo change, data migration |
| High uncertainty, novel technology | **Iterative** — plan first spike/prototype, defer detailed planning until after learning | Evaluating new tool, experimental feature, POC |

### When to Re-Plan

Trigger a plan revision when:
- A key assumption is invalidated
- Scope changes by >20%
- A critical dependency becomes unavailable
- The dominant uncertainty type shifts (e.g., ambiguity resolves into concrete risks)
- Stakeholder priorities change

---

## Cross-References

- See `rules/design-patterns.md` for architectural decision guidance
- See `rules/knowledge-management.md` for knowledge creation cycle (plans generate knowledge that should be captured)
