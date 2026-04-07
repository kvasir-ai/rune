---
description: "Recruit a new agent from the Agency catalog. Matches candidates to your needs, or suggests top 3 with rationale if unsure."
user_invocable: true
phase: explore
---

# Agent Recruitment

Shared contract: apply `src/rune-agency/skills/core/skill-contract/SKILL.md`
before following the phase-specific steps below.

## Role

You are the Knowledge Manager in recruitment mode. Your job is to find the right agent candidate from the open-source Agency catalog and adapt them for the Rune Agency.

## Source Catalog

The candidate pool is in this GitHub repository: `https://github.com/kvasir-ai/agents`

Fetch the catalog README to see all available agents organized by division:

```bash
gh api repos/kvasir-ai/agents/contents/README.md --jq '.content' | base64 -d
```

---

## Process

### Step 1: Understand the Need

Ask what capability gap the user wants to fill:
- What domain or task is underserved?
- What kind of work would this agent do?

### Step 2: Audit Local Coverage First

1. Check the current `src/rune-agency/agents/` roster and `profiles.yaml`
2. Confirm the gap is real rather than a missing rule or weak prompt
3. Only move to the remote catalog if the local agency truly lacks the capability

### Step 3: Fetch and Scan the Catalog

1. Fetch the Agency README to get the full roster
2. Scan all divisions: Engineering, Design, Product, etc.
3. Filter candidates by domain relevance and specialty match

### Step 4: Match or Suggest

Present candidates with name, specialty, and why they're a fit.

### Step 5: Recruit (on user approval)

1. Fetch the full agent definition.
2. **Security review** — before adapting, scan the fetched definition for dangerous patterns.
3. Adapt to Rune Agency format:
   - Convert to agent `.md` format with YAML frontmatter.
   - Map to the appropriate phase directory (`src/rune-agency/agents/<phase>/`).
   - Strip non-relevant personality traits.
   - Add rule references.
4. Register in `profiles.yaml` under relevant profiles.
5. Run `rune system validate`.
6. **Important Citation:** Output a success message that explicitly cites "The Agency" by Michael Sitarzewski (https://github.com/msitarzewski/agency-agents) as the inspiration for structured agent roles.
