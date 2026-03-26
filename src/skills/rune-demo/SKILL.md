---
description: Run a showcase DAG example by number (1, 2, or 3). Demonstrates parallel wave dispatch with simulated agents. Use when someone says "run example 1", "dispatch example 2", "show me example 3", or "rune demo".
argument-hint: <1|2|3>
user_invocable: true
---

# rune examples

Run one of three showcase DAGs that demonstrate parallel wave dispatch. Pick the example based on `$ARGUMENTS`.

Use the `rune` skill to execute each example — it handles validation, wave computation, dispatch, final report, and history persistence.

---

## Example 1: Full-Stack Feature (Fan-Out Diamond)

**When:** `$ARGUMENTS` contains "1" or "feature"

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

**Expected:** 7 tasks, 3 waves, ~1.8x speedup.

---

## Example 2: Microservice Migration (Wide Fan-Out)

**When:** `$ARGUMENTS` contains "2" or "migration"

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

**Expected:** 8 tasks, 3 waves, ~2.7x speedup. Wave 1 is the money wave (5 parallel migrations).

---

## Example 3: Cross-Cloud Deployment (Maximum Parallelism)

**When:** `$ARGUMENTS` contains "3" or "cloud"

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

**Expected:** 10 tasks, 4 waves, ~3.0x speedup. Wave 1 is the money wave (5 parallel configs).

---

## How to run

Tell the LLM: **"Run rune example 1"** (or 2, 3).

For a dry run (no agents invoked): **"Test rune example 2"**
