---
name: rune-examples
description: Run a showcase DAG example by number (1, 2, or 3). Demonstrates parallel wave dispatch with simulated agents. Use when someone says "run example 1", "dispatch example 2", "show me example 3", or "rune demo".
argument-hint: <1|2|3>
---

# rune examples

Run one of three showcase DAGs that demonstrate parallel wave dispatch.

Pick the example based on `$ARGUMENTS`:

## Example 1: Full-Stack Feature (Fan-Out Diamond)

**When:** `$ARGUMENTS` contains "1" or "feature"

Use the `executing-dag-plans` skill with this plan:

```yaml
tasks:
  - id: t1
    agent: architect
    title: Design API contract
    depends_on: []
    files: [docs/api-contract.yaml]
    output: API schema with endpoints, request/response types, and error codes

  - id: t2
    agent: designer
    title: Design UI components
    depends_on: []
    files: [src/components/]
    output: Component hierarchy, props interfaces, and wireframe descriptions

  - id: t3
    agent: developer
    title: Set up database schema
    depends_on: []
    files: [migrations/]
    output: SQL migration files for the feature's data model

  - id: t4
    agent: writer
    title: Draft user documentation
    depends_on: []
    files: [docs/user-guide.md]
    output: End-user documentation for the new feature

  - id: t5
    agent: developer
    title: Implement API and UI
    depends_on: [t1, t2, t3]
    files: [src/api/, src/ui/]
    output: Working API endpoints and UI components wired together

  - id: t6
    agent: tester
    title: Write test plan and tests
    depends_on: [t1, t3]
    files: [tests/]
    output: Test plan document and test files covering API and data layer

  - id: t7
    agent: reviewer
    title: Final code review
    depends_on: [t4, t5, t6]
    files: []
    output: Review summary with approval or change requests
```

**Expected waves:**
- Wave 0: t1, t2, t3, t4 (4 parallel)
- Wave 1: t5, t6 (2 parallel)
- Wave 2: t7
- **Speedup: ~1.8x** (13 min parallel vs 24 min sequential)

---

## Example 2: Microservice Migration (Wide Fan-Out)

**When:** `$ARGUMENTS` contains "2" or "migration"

Use the `executing-dag-plans` skill with this plan:

```yaml
tasks:
  - id: t1
    agent: architect
    title: Define shared types and interfaces
    depends_on: []
    files: [shared/types/]
    output: Shared type definitions, interface contracts, and versioning strategy

  - id: t2
    agent: developer
    title: Migrate auth service
    depends_on: [t1]
    files: [services/auth/]
    output: Migrated auth service with updated type imports

  - id: t3
    agent: developer
    title: Migrate billing service
    depends_on: [t1]
    files: [services/billing/]
    output: Migrated billing service with updated type imports

  - id: t4
    agent: developer
    title: Migrate notifications service
    depends_on: [t1]
    files: [services/notifications/]
    output: Migrated notifications service with updated type imports

  - id: t5
    agent: developer
    title: Migrate analytics service
    depends_on: [t1]
    files: [services/analytics/]
    output: Migrated analytics service with updated type imports

  - id: t6
    agent: developer
    title: Migrate user service
    depends_on: [t1]
    files: [services/users/]
    output: Migrated user service with updated type imports

  - id: t7
    agent: tester
    title: Integration tests across all services
    depends_on: [t2, t3, t4, t5, t6]
    files: [tests/integration/]
    output: Cross-service integration test suite

  - id: t8
    agent: security
    title: Security audit of all services
    depends_on: [t2, t3, t4, t5, t6]
    files: [docs/security-audit.md]
    output: Security audit report covering auth flows, data handling, and API exposure
```

**Expected waves:**
- Wave 0: t1 (1 task — setup)
- Wave 1: t2, t3, t4, t5, t6 (5 parallel — the money wave)
- Wave 2: t7, t8 (2 parallel)
- **Speedup: ~2.7x** (18 min parallel vs 48 min sequential)

---

## Example 3: Cross-Cloud Deployment (Maximum Parallelism)

**When:** `$ARGUMENTS` contains "3" or "cloud"

Use the `executing-dag-plans` skill with this plan:

```yaml
tasks:
  - id: t1
    agent: architect
    title: Define infrastructure-as-code modules
    depends_on: []
    files: [infra/modules/]
    output: Shared IaC modules for compute, networking, and storage

  - id: t2
    agent: developer
    title: Configure AWS deployment
    depends_on: [t1]
    files: [infra/aws/]
    output: AWS-specific IaC with VPC, ECS, and RDS configuration

  - id: t3
    agent: developer
    title: Configure GCP deployment
    depends_on: [t1]
    files: [infra/gcp/]
    output: GCP-specific IaC with VPC, Cloud Run, and Cloud SQL configuration

  - id: t4
    agent: developer
    title: Configure Azure deployment
    depends_on: [t1]
    files: [infra/azure/]
    output: Azure-specific IaC with VNet, Container Apps, and Azure SQL configuration

  - id: t5
    agent: writer
    title: Write deployment runbook
    depends_on: [t1]
    files: [docs/runbook.md]
    output: Operator runbook covering deploy, rollback, and incident response per cloud

  - id: t6
    agent: security
    title: Threat model all three clouds
    depends_on: [t1]
    files: [docs/threat-model.md]
    output: Threat model covering IAM, network boundaries, and data encryption per provider

  - id: t7
    agent: tester
    title: Validate AWS deployment
    depends_on: [t2]
    files: [tests/aws/]
    output: AWS integration test results and cost estimate

  - id: t8
    agent: tester
    title: Validate GCP deployment
    depends_on: [t3]
    files: [tests/gcp/]
    output: GCP integration test results and cost estimate

  - id: t9
    agent: tester
    title: Validate Azure deployment
    depends_on: [t4]
    files: [tests/azure/]
    output: Azure integration test results and cost estimate

  - id: t10
    agent: devops
    title: Publish multi-cloud release
    depends_on: [t5, t6, t7, t8, t9]
    files: []
    output: Published release with deployment artifacts, runbook, and security sign-off
```

**Expected waves:**
- Wave 0: t1 (1 task — shared modules)
- Wave 1: t2, t3, t4, t5, t6 (5 parallel — the money wave)
- Wave 2: t7, t8, t9 (3 parallel — validation)
- Wave 3: t10 (1 task — publish)
- **Speedup: ~3.0x** (15 min parallel vs 45 min sequential)

---

## Example 4: Full SSDLC Cycle (Idea to Ship)

**When:** `$ARGUMENTS` contains "4" or "ssdlc" or "lifecycle"

This example demonstrates the complete Secure Software Development Lifecycle:
**Idea → Plan → WBS → Judge → Implement → Judge → Ship**

Use the `executing-dag-plans` skill with this plan:

```yaml
tasks:
  # --- Stage 1: Idea ---
  - id: t1
    agent: architect
    title: Brainstorm and design the feature
    depends_on: []
    files: [docs/design.md]
    output: Design document with requirements, constraints, API contract, and component diagram

  # --- Stage 2: Plan ---
  - id: t2
    agent: planner
    title: Write implementation plan from design
    depends_on: [t1]
    files: [docs/plans/]
    output: Step-by-step TDD implementation plan with atomic tasks, dependencies, and acceptance criteria

  # --- Stage 3: Judge the Plan ---
  - id: t3
    agent: judge
    title: Validate plan completeness and safety
    depends_on: [t2]
    files: []
    output: Judge verdict on plan — APPROVED, APPROVED WITH WARNINGS, or BLOCKED

  # --- Stage 4: Implement (parallel WBS) ---
  - id: t4
    agent: developer
    title: Implement core business logic
    depends_on: [t3]
    files: [src/core/]
    output: Core module with unit tests passing

  - id: t5
    agent: developer
    title: Implement API layer
    depends_on: [t3]
    files: [src/api/]
    output: API endpoints with request validation and error handling

  - id: t6
    agent: developer
    title: Implement persistence layer
    depends_on: [t3]
    files: [src/storage/]
    output: Database schema, migrations, and repository pattern implementation

  - id: t7
    agent: technical-writer
    title: Write user documentation
    depends_on: [t3]
    files: [docs/user-guide.md]
    output: End-user documentation covering setup, usage, and troubleshooting

  # --- Stage 5: Quality Gates (parallel) ---
  - id: t8
    agent: tester
    title: Write integration tests across all layers
    depends_on: [t4, t5, t6]
    files: [tests/integration/]
    output: Integration test suite covering API-to-storage flows

  - id: t9
    agent: security
    title: Security review of implementation
    depends_on: [t4, t5, t6]
    files: [docs/security-review.md]
    output: Security assessment covering auth, input validation, and data protection

  - id: t10
    agent: reviewer
    title: Code review of entire implementation
    depends_on: [t4, t5, t6]
    files: []
    output: Code review report with approval or change requests

  # --- Stage 6: Final Judgment ---
  - id: t11
    agent: judge
    title: Final validation — is this ready to ship?
    depends_on: [t7, t8, t9, t10]
    files: []
    output: Final judge verdict on implementation quality, test coverage, security posture, and documentation completeness

  # --- Stage 7: Ship ---
  - id: t12
    agent: devops
    title: Prepare release artifacts and publish
    depends_on: [t11]
    files: []
    output: Release artifacts, changelog entry, and deployment confirmation
```

**Expected waves:**
- Wave 0: t1 (1 task — brainstorm/design)
- Wave 1: t2 (1 task — plan from design)
- Wave 2: t3 (1 task — judge validates plan)
- Wave 3: t4, t5, t6, t7 (4 parallel — the implementation wave)
- Wave 4: t8, t9, t10 (3 parallel — quality gates)
- Wave 5: t11 (1 task — final judgment)
- Wave 6: t12 (1 task — ship)
- **Speedup: ~1.7x** (7 waves vs 12 sequential tasks)

**SSDLC stages visualized:**

```
  Idea        Plan       Judge       Implement          Quality         Judge    Ship
   t1    →     t2    →    t3    →  t4,t5,t6,t7  →   t8,t9,t10    →    t11   →  t12
 design      plan      validate    build in         test/security     final     release
                                   parallel         review in         verdict
                                                    parallel
```

---

## How to run

Tell the LLM: **"Run rune example 1"** (or 2, 3, or 4).

The `executing-dag-plans` skill will:
1. Parse the YAML task list
2. Validate the DAG (cycle detection, file scope conflicts)
3. Compute waves via topological sort
4. Display the dispatch plan with agent emojis
5. Execute wave by wave, dispatching parallel tasks simultaneously
6. Produce a final status report

For a dry run (no agents invoked): **"Test rune example 2"**
