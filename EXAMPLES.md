# DAG Dispatch Examples

Three showcase DAGs demonstrating parallel wave dispatch — from simple to maximum parallelism. Each shows the full lifecycle: dispatch diagram, wave execution, final report, and history persistence.

Run any example by saying: **"run rune example 1"** (or 2, 3). Dry-run with **"test rune example 1"**.

---

## Example 1: Full-Stack Feature

**Pattern:** Fan-out diamond. 4 independent tasks start together, converge through implementation, single review gate.

### Dispatch Diagram

```
───────────────────────────────────────────
  DAG DISPATCH PLAN
  Tasks: 7  |  Waves: 3  |  Benefit: 1.8x
───────────────────────────────────────────

  Wave 0  ─── 4 parallel ──────────────────
  🏗️  t1  architect         Design API contract
  🎨  t2  designer          Design UI components
  🔧  t3  developer         Set up database schema
  ✍️  t4  writer            Draft user documentation

  Wave 1  ─── 2 parallel ──────────────────
  🔧  t5  developer         Implement API and UI
                              ↳ depends on: t1, t2, t3
  🧪  t6  tester            Write test plan and tests
                              ↳ depends on: t1, t3

  Wave 2  ────────────────────────────────
  🔍  t7  reviewer          Final code review
                              ↳ depends on: t4, t5, t6

───────────────────────────────────────────
  Critical path: t1 → t5 → t7
  Path length: 3 of 7 tasks (43%)
───────────────────────────────────────────
```

### Wave Execution

```
═══ Wave 0: Dispatching 4 agents ══════════
  🏗️  t1 → architect         Design API contract
  🎨  t2 → designer          Design UI components
  🔧  t3 → developer         Set up database schema
  ✍️  t4 → writer            Draft user documentation
═══════════════════════════════════════════
```

```
═══ Wave 1: Dispatching 2 agents ══════════
  🔧  t5 → developer         Implement API and UI
  🧪  t6 → tester            Write test plan and tests
═══════════════════════════════════════════
```

```
═══ Wave 2: Dispatching 1 agent ═══════════
  🔍  t7 → reviewer          Final code review
═══════════════════════════════════════════
```

### Final Report

```
───────────────────────────────────────────
  DAG EXECUTION COMPLETE
───────────────────────────────────────────

  Wave 0  ─── 4 agents ──────────────────
  🏗️  t1  architect       ✅ API contract defined
  🎨  t2  designer        ✅ Components designed
  🔧  t3  developer       ✅ Schema migrated
  ✍️  t4  writer          ✅ Docs drafted

  Wave 1  ─── 2 agents ──────────────────
  🔧  t5  developer       ✅ API + UI implemented
  🧪  t6  tester          ✅ Tests written

  Wave 2  ────────────────────────────────
  🔍  t7  reviewer        ✅ Approved

───────────────────────────────────────────
  Tasks:  7/7 completed  |  0 failed
  Waves:  3 executed     |  2 had parallelism
  Saved:  ~44% vs sequential
───────────────────────────────────────────
  📋 Saved to .rune/2026-03-23T10-00-00-full-stack-feature.yaml
───────────────────────────────────────────
```

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

### Dispatch Diagram

```
───────────────────────────────────────────
  DAG DISPATCH PLAN
  Tasks: 8  |  Waves: 3  |  Benefit: 2.7x
───────────────────────────────────────────

  Wave 0  ────────────────────────────────
  🏗️  t1  architect         Define shared types

  Wave 1  ─── 5 parallel ──────────────────
  🔧  t2  developer         Migrate auth service
                              ↳ depends on: t1
  🔧  t3  developer         Migrate billing service
                              ↳ depends on: t1
  🔧  t4  developer         Migrate notifications
                              ↳ depends on: t1
  🔧  t5  developer         Migrate analytics
                              ↳ depends on: t1
  🔧  t6  developer         Migrate user service
                              ↳ depends on: t1

  Wave 2  ─── 2 parallel ──────────────────
  🧪  t7  tester            Integration tests
                              ↳ depends on: t2, t3, t4, t5, t6
  🔒  t8  security          Security audit
                              ↳ depends on: t2, t3, t4, t5, t6

───────────────────────────────────────────
  Critical path: t1 → t2 → t7
  Path length: 3 of 8 tasks (38%)
───────────────────────────────────────────
```

### Final Report

```
───────────────────────────────────────────
  DAG EXECUTION COMPLETE
───────────────────────────────────────────

  Wave 0  ────────────────────────────────
  🏗️  t1  architect       ✅ Shared types defined

  Wave 1  ─── 5 agents ──────────────────
  🔧  t2  developer       ✅ Auth migrated
  🔧  t3  developer       ✅ Billing migrated
  🔧  t4  developer       ✅ Notifications migrated
  🔧  t5  developer       ✅ Analytics migrated
  🔧  t6  developer       ✅ Users migrated

  Wave 2  ─── 2 agents ──────────────────
  🧪  t7  tester          ✅ All integration tests pass
  🔒  t8  security        ✅ No vulnerabilities found

───────────────────────────────────────────
  Tasks:  8/8 completed  |  0 failed
  Waves:  3 executed     |  2 had parallelism
  Saved:  ~63% vs sequential
───────────────────────────────────────────
  📋 Saved to .rune/2026-03-23T11-00-00-microservice-migration.yaml
───────────────────────────────────────────
```

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

## Example 3: Cross-Cloud Deployment (with partial failure)

**Pattern:** Maximum parallelism. Shared IaC modules, then 3 cloud configs + docs + security in parallel, per-cloud validation, single publish. Demonstrates failure handling.

### Dispatch Diagram

```
───────────────────────────────────────────
  DAG DISPATCH PLAN
  Tasks: 10  |  Waves: 4  |  Benefit: 3.0x
───────────────────────────────────────────

  Wave 0  ────────────────────────────────
  🏗️  t1  architect         Define IaC modules

  Wave 1  ─── 5 parallel ──────────────────
  🔧  t2  developer         Configure AWS deployment
                              ↳ depends on: t1
  🔧  t3  developer         Configure GCP deployment
                              ↳ depends on: t1
  🔧  t4  developer         Configure Azure deployment
                              ↳ depends on: t1
  ✍️  t5  writer            Write deployment runbook
                              ↳ depends on: t1
  🔒  t6  security          Threat model all clouds
                              ↳ depends on: t1

  Wave 2  ─── 3 parallel ──────────────────
  🧪  t7  tester            Validate AWS
                              ↳ depends on: t2
  🧪  t8  tester            Validate GCP
                              ↳ depends on: t3
  🧪  t9  tester            Validate Azure
                              ↳ depends on: t4

  Wave 3  ────────────────────────────────
  🚀  t10 devops            Publish multi-cloud release
                              ↳ depends on: t5, t6, t7, t8, t9

───────────────────────────────────────────
  Critical path: t1 → t2 → t7 → t10
  Path length: 4 of 10 tasks (40%)
───────────────────────────────────────────
```

### Wave 2: Azure Validation Fails

```
═══ Wave 2: Dispatching 3 agents ══════════
  🧪  t7 → tester            Validate AWS
  🧪  t8 → tester            Validate GCP
  🧪  t9 → tester            Validate Azure
═══════════════════════════════════════════
```

```
───────────────────────────────────────────
  ❌ Task t9 FAILED
───────────────────────────────────────────
  Agent:   tester
  Error:   Azure Container Apps quota
           exceeded in westeurope region

  Blocked: t10 (devops)
  Still OK: t7 (completed), t8 (completed)

  Options:
    1. Retry t9
    2. Skip t9, continue with unblocked
    3. Halt execution
───────────────────────────────────────────
```

### Final Report (Partial)

```
───────────────────────────────────────────
  DAG EXECUTION COMPLETE
───────────────────────────────────────────

  Wave 0  ────────────────────────────────
  🏗️  t1  architect       ✅ IaC modules defined

  Wave 1  ─── 5 agents ──────────────────
  🔧  t2  developer       ✅ AWS configured
  🔧  t3  developer       ✅ GCP configured
  🔧  t4  developer       ✅ Azure configured
  ✍️  t5  writer          ✅ Runbook written
  🔒  t6  security        ✅ Threat model complete

  Wave 2  ─── 3 agents ──────────────────
  🧪  t7  tester          ✅ AWS validated
  🧪  t8  tester          ✅ GCP validated
  🧪  t9  tester          ❌ Azure quota exceeded

  Wave 3  ────────────────────────────────
  🚀  t10 devops          ⛔ BLOCKED (t9 failed)

───────────────────────────────────────────
  Tasks:  8/10 completed  |  1 failed  |  1 blocked
  Waves:  3 of 4 executed
───────────────────────────────────────────
  📋 Saved to .rune/2026-03-23T14-00-00-cross-cloud-deploy.yaml
───────────────────────────────────────────
```

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

| Example | Scenario | Tasks | Waves | Speedup | Shows |
|---|---|---|---|---|---|
| 1 | Full-Stack Feature | 7 | 3 | **1.8x** | Fan-out diamond, full success |
| 2 | Microservice Migration | 8 | 3 | **2.7x** | Wide fan-out (5 parallel) |
| 3 | Cross-Cloud Deployment | 10 | 4 | **3.0x** | Maximum parallelism, partial failure |

The wider the wave, the bigger the savings. Write your own DAGs in the same YAML format — see [DAG Execution Format](src/rules/collaboration/dag-execution-format.md) for the full spec.

---

## Formatting Reference

### Frame Styles

| Context | Character | Width | Purpose |
|---|---|---|---|
| Planning (dispatch diagram, final report) | `───` (light) | 43 chars | Static — showing structure |
| Execution (wave banners) | `═══` (double) | 43 chars | Active — action happening now |

### Task Row Formats

| Context | Format |
|---|---|
| Pre-dispatch | `{emoji}  {id}  {agent}  {description}` |
| Execution | `{emoji}  {id} → {agent}  {description}` |
| Final report | `{emoji}  {id}  {agent}  {status} {summary}` |

The `→` arrow appears ONLY in execution banners — it signals "action happening now."

### Status Indicators

| Emoji | Meaning |
|---|---|
| ✅ | Task completed successfully |
| ❌ | Task failed |
| ⛔ | Blocked — dependency failed |
| ⏭️ | Skipped by user |

### History Persistence

Every dispatch writes to `.rune/` in the project root (gitignored by default):

```
.rune/
  2026-03-23T10-00-00-full-stack-feature.yaml
  2026-03-23T11-00-00-microservice-migration.yaml
  2026-03-23T14-00-00-cross-cloud-deploy.yaml
```

Summaries only — never raw agent output.
