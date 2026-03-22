# DAG Dispatch Examples

Three showcase DAGs demonstrating parallel wave dispatch — from simple to maximum parallelism.

Run any example by saying: **"run rune example 1"** (or 2, 3). Dry-run with **"test rune example 1"**.

---

## Example 1: Full-Stack Feature

**Pattern:** Fan-out diamond. 4 independent tasks start together, converge through implementation, single review gate.

```
  Wave 0  ─── 4 parallel ────────────────
  🏗️  architect       Design API contract
  🎨  designer        Design UI components
  🔧  developer       Set up database schema
  ✍️  writer          Draft user documentation

  Wave 1  ─── 2 parallel ────────────────
  🔧  developer       Implement API and UI
  🧪  tester          Write test plan and tests

  Wave 2  ────────────────────────────────
  🔍  reviewer        Final code review
```

**Tasks:** 7 | **Waves:** 3 | **Speedup:** 1.8x (13 min vs 24 min sequential)

<details>
<summary>Full YAML</summary>

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
</details>

---

## Example 2: Microservice Migration

**Pattern:** Wide fan-out. One setup task, then 5 independent migrations in parallel, then validation.

```
  Wave 0  ────────────────────────────────
  🏗️  architect       Define shared types and interfaces

  Wave 1  ─── 5 parallel (the money wave)
  🔧  developer       Migrate auth service
  🔧  developer       Migrate billing service
  🔧  developer       Migrate notifications service
  🔧  developer       Migrate analytics service
  🔧  developer       Migrate user service

  Wave 2  ─── 2 parallel ────────────────
  🧪  tester          Integration tests (all services)
  🔒  security        Security audit (all services)
```

**Tasks:** 8 | **Waves:** 3 | **Speedup:** 2.7x (18 min vs 48 min sequential)

<details>
<summary>Full YAML</summary>

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
</details>

---

## Example 3: Cross-Cloud Deployment

**Pattern:** Maximum parallelism. Shared IaC modules, then 3 cloud configs + docs + security in parallel, per-cloud validation, single publish.

```
  Wave 0  ────────────────────────────────
  🏗️  architect       Define IaC modules

  Wave 1  ─── 5 parallel (the money wave)
  🔧  developer       Configure AWS deployment
  🔧  developer       Configure GCP deployment
  🔧  developer       Configure Azure deployment
  ✍️  writer          Write deployment runbook
  🔒  security        Threat model all three clouds

  Wave 2  ─── 3 parallel ────────────────
  🧪  tester          Validate AWS deployment
  🧪  tester          Validate GCP deployment
  🧪  tester          Validate Azure deployment

  Wave 3  ────────────────────────────────
  🚀  devops          Publish multi-cloud release
```

**Tasks:** 10 | **Waves:** 4 | **Speedup:** 3.0x (15 min vs 45 min sequential)

<details>
<summary>Full YAML</summary>

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
</details>

---

## Comparison

| Example | Scenario | Tasks | Waves | Speedup | Best for |
|---|---|---|---|---|---|
| 1 | Full-Stack Feature | 7 | 3 | **1.8x** | Everyday feature work |
| 2 | Microservice Migration | 8 | 3 | **2.7x** | Refactoring at scale |
| 3 | Cross-Cloud Deployment | 10 | 4 | **3.0x** | Infrastructure teams |

The wider the wave, the bigger the savings. Write your own DAGs in the same YAML format — see [DAG Execution Format](src/rules/collaboration/dag-execution-format.md) for the full spec.
