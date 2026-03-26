# DAG Dispatch Examples

Three example plans show how parallel dispatch works. They go from simple to complex. Each one shows the full cycle: plan, execution, final report, and saved history.

A DAG (directed acyclic graph) is a set of tasks with dependencies between them. Tasks that don't depend on each other run at the same time in "waves."

Try any example: **"run rune example 1"** (or 2, 3). Dry-run with **"test rune example 1"**.

---

## Example 1: Full-Stack Feature

**Pattern:** Fan-out diamond. Four tasks start at the same time. They feed into two implementation tasks. One review task finishes the job.

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
  💰 Token Economics
───────────────────────────────────────────
  t1  architect       310K tok   $6.51
  t2  designer        285K tok   $5.99
  t3  developer       340K tok   $7.14
  t4  writer          295K tok   $6.20
  t5  developer       380K tok   $7.98
  t6  tester          320K tok   $6.72
  t7  reviewer        290K tok   $6.09
───────────────────────────────────────────
  Total tokens:  2,220K  (2,220,000)
  Est. cost:     $46.63
  Avg per agent: $6.66
  Wall time:     7m 45s  (parallel)
  CPU time:      13m 52s (sequential sum)
  Time saved:    44% via parallelism
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

**Pattern:** Wide fan-out. One setup task runs first. Then five independent migrations run at the same time. Then validation.

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
  💰 Token Economics
───────────────────────────────────────────
  t1  architect       350K tok   $7.35
  t2  developer       290K tok   $6.09
  t3  developer       315K tok   $6.62
  t4  developer       305K tok   $6.41
  t5  developer       365K tok   $7.67
  t6  developer       340K tok   $7.14
  t7  tester          380K tok   $7.98
  t8  security        310K tok   $6.51
───────────────────────────────────────────
  Total tokens:  2,655K  (2,655,000)
  Est. cost:     $55.77
  Avg per agent: $6.97
  Wall time:     9m 20s  (parallel)
  CPU time:      25m 12s (sequential sum)
  Time saved:    63% via parallelism
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

**Pattern:** Maximum parallelism. One shared setup, then five tasks run at once (three cloud configs plus docs plus security). Per-cloud validation follows. A single publish step finishes the job. This example also shows what happens when a task fails.

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

Azure validation hits a quota limit. The other two validations finish fine. The publish step (t10) is blocked because it depends on t9.

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

The report shows which tasks passed, which failed, and which were blocked.

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
  💰 Token Economics
───────────────────────────────────────────
  t1  architect       340K tok   $7.14
  t2  developer       310K tok   $6.51
  t3  developer       325K tok   $6.83
  t4  developer       315K tok   $6.62
  t5  devops          290K tok   $6.09
  t6  devops          285K tok   $5.99
  t7  tester          350K tok   $7.35
  t8  tester          330K tok   $6.93
  t9  tester          ❌       —       —
  t10 devops          ⛔       —       —
───────────────────────────────────────────
  Total tokens:  2,545K  (completed only)
  Est. cost:     $53.46
  Wall time:     11m 05s
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

| Example | Scenario | Tasks | Waves | Speedup | What it shows |
|---|---|---|---|---|---|
| 1 | Full-Stack Feature | 7 | 3 | **1.8x** | Fan-out diamond, all tasks pass |
| 2 | Microservice Migration | 8 | 3 | **2.7x** | Wide fan-out (5 tasks at once) |
| 3 | Cross-Cloud Deployment | 10 | 4 | **3.0x** | Maximum parallelism, one task fails |

Wider waves save more time. You can write your own DAGs in the same YAML format. See [DAG Execution Format](src/rules/collaboration/dag-execution-format.md) (internal specification — this is the agent-facing reference for the DAG format) for the full spec.
