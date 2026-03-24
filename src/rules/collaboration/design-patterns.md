# Design Patterns Reference

> Pattern selection guidance for all engineering agents.
> Consult the Developer agent for language-specific patterns, Code Reviewer for pattern review.
> Go and Python examples are illustrative — apply the same principles to any language.

---

## When NOT to Use Patterns

- **Over-engineering**: Adding patterns to simple problems — three similar lines are better than a premature abstraction
- **Pattern hunting**: Looking for places to apply patterns you just learned
- **Premature flexibility**: Adding configurability you don't need yet
- **Copy-paste patterns**: Using patterns without understanding the problem they solve

---

## Problem-to-Pattern Quick Reference

### Object Creation
| Problem | Pattern | Example |
|---|---|---|
| Multiple construction variations | Builder | Complex gRPC request construction |
| Expensive object creation | Prototype | Database client pooling |
| Family of related objects | Abstract Factory | Multi-stage environment config |
| Decoupled object creation | Factory Method | Message consumer instantiation per domain |

### Structural
| Problem | Pattern | Example |
|---|---|---|
| Interface incompatibility | Adapter | Legacy API wrapping for new services |
| Adding behavior without inheritance | Decorator | Middleware chains (auth, logging, metrics) |
| Simplifying complex subsystems | Facade | Database client wrapper for common operations |
| Controlling access | Proxy | Rate-limited API clients, caching proxies |

### Behavioral
| Problem | Pattern | Example |
|---|---|---|
| One-to-many notifications | Observer | Event bus publishing |
| Algorithm variations | Strategy | Different pricing/fee calculation strategies |
| Undo/redo, queued operations | Command | Approval workflow automation |
| State-dependent behavior | State | Order lifecycle state machine |
| Sequential processing | Chain of Responsibility | Request validation pipeline |

---

## Microservices Patterns

### Communication
- **API Gateway**: API gateway for routing, CDN/WAF for public APIs
- **Service Mesh**: mTLS between product services
- **Event Sourcing**: Event log → data warehouse tables (append-only history)
- **CQRS**: Separate read (analytics marts) from write (gRPC services) paths

### Data Management
- **Database per Service**: Relational DB per domain, separate analytics store for reporting
- **Saga Pattern**: Distributed transaction coordination across billing/order services
- **Event Store**: Message topics as immutable event log, streaming pipeline writes to analytics store

### Service Decomposition
- **Bounded contexts**: Each domain (orders, billing, inventory, accounts) maps to a bounded context with clear data ownership
- **Service capability mapping**: Define what each service owns (data entities, operations, dependencies)
- **Coupling analysis**: If two services share data entities or have bidirectional dependencies, consider merging or introducing an event-based boundary

### Distributed Transactions
- **Saga pattern**: Orchestrate multi-service transactions with compensation steps (e.g., reserve inventory → process payment → confirm order; if payment fails → release inventory)
- **Choreography vs orchestration**: Prefer choreography (event-driven) for simple flows, orchestration for complex multi-step sagas with compensation logic
- **Idempotency**: All saga steps must be idempotent — retries must be safe

### Operational Patterns
- **Health checks**: Liveness (is the process alive?) + readiness (can it accept traffic?) — both required for container deployments
- **Service discovery**: DNS-based discovery is the default — no custom service registry needed
- **Observability**: Structured logging, distributed tracing (OTel OTLP), Prometheus metrics

### Resilience (Cloud-Native)
- **Circuit Breaker**: Fail fast on downstream service failures
- **Retry with Backoff**: Handle transient failures from external services
- **Bulkhead**: Consumer domain splits isolate blast radius
- **Timeout**: Prevent hanging queries or gRPC calls

---

## Anti-Patterns to Flag in Code Review

| Anti-Pattern | Symptoms | Fix |
|---|---|---|
| God Object | Class >500 lines, handles auth + validation + persistence + notification | Split by Single Responsibility |
| Spaghetti Code | Methods >50 lines, unclear dependencies, no structure | Apply Facade/Strategy, extract methods |
| Lava Flow | Dead code, commented-out blocks, unused functions | Delete it — git has history |
| Primitive Obsession | Passing raw strings/ints where domain types belong | Introduce value objects |
| Shotgun Surgery | One change requires edits in 10+ files | Consolidate related logic |
| Feature Envy | Method uses another class's data more than its own | Move method to where the data lives |

---

## Testing Patterns

### Test Strategy
| Layer | Scope | When |
|---|---|---|
| Integration | Module interactions, API contracts, DB queries, message consumers | Primary focus — test real interactions between components |
| E2E / Smoke | Critical user journeys, deployment validation, cross-service flows | Verify the system works end-to-end after deployment |
| Unit | Business logic, domain rules, calculations | Test business rules — not machinery, glue code, or framework wiring |

### Test Doubles
- **Mock**: Verify behavior (e.g., "was this message published?")
- **Stub**: Return fixed data (e.g., fake query results)
- **Fake**: Lightweight implementation (e.g., in-memory store instead of the relational database)
- **Spy**: Record interactions for assertion

### Test Structure
- **AAA**: Arrange → Act → Assert (standard for unit tests)
- **Given-When-Then**: BDD style for integration/acceptance tests
- Use real databases for integration tests where possible (not mocks)

### Test Data
- **Factories**: Use factory functions to create test entities with sensible defaults and easy overrides
- **Fixtures**: Shared test data for common scenarios (edge cases, boundary values, special characters)
- **Scenario builders**: Compose complex test setups from simpler factories
- **No PII in test data**: Use synthetic/anonymized data — never copy production PII into test fixtures

### Quality Gates (CI/CD)
- Integration and E2E tests must pass before merge
- Flaky tests must be fixed or quarantined — never ignored
- Performance tests run on backend changes (prevent regression)

---

## Clean Architecture Principles

### Dependency Rule
- Dependencies point **inward** toward core business logic
- Inner layers (domain, use cases) know nothing about outer layers (HTTP, database, message broker)
- Business rules are independent of frameworks, UI, and databases

### Layer Structure
| Layer | Contains | Example |
|---|---|---|
| **Domain** | Business rules, entities, value objects | Order lifecycle, cost calculation, fee rules |
| **Use Cases** | Application logic, orchestration | CreateOrder, ProcessBilling, CalculateTotal |
| **Adapters** | Controllers, repositories, gateways | HTTP handlers, DB repos, event publishers |
| **Infrastructure** | Frameworks, drivers, external services | HTTP server, DB client, message broker SDK |

### When to Apply
- **Yes**: New microservices, complex domain logic, services with multiple adapters (REST + gRPC + messaging)
- **Maybe**: Batch jobs with simple input→process→output flows
- **No**: Simple scripts, one-off utilities — over-engineering

### Key Practices
- Define repository interfaces in the domain/use-case layer, implement in the adapter layer
- Use dependency injection — constructor injection preferred over service locators
- Domain exceptions (e.g., `InsufficientStockError`) stay in the domain layer; adapters translate to HTTP/gRPC status codes
- Test domain logic without any infrastructure dependencies

---

## Functional Patterns (Go & Python)

### Go
- **Options pattern**: Functional options for flexible constructors (`WithTimeout(5s)`, `WithRetries(3)`)
- **Error wrapping**: `fmt.Errorf("operation failed: %w", err)` for context chain
- **Context propagation**: Pass `context.Context` for cancellation and deadlines
- **Table-driven tests**: Test cases as data, loop over them

### Python
- **Dataclasses**: Prefer over dicts for structured data
- **Result pattern**: Return `(value, error)` tuples or use Result types for expected failures
- **Generator pipelines**: Chain generators for memory-efficient data processing

---

## Performance Optimization

### Databases and Analytics
- **Partition pruning**: Always filter on partition columns — avoid full table scans
- **Clustering/indexing**: Index high-cardinality filter columns
- **SELECT only needed columns**: Columnar stores charge per column scanned — avoid `SELECT *`
- **Materialized views**: For frequently-run aggregations that don't need real-time freshness

### Go Services
- **Profiling**: `pprof` for CPU and memory profiling
- **Connection pooling**: Reuse gRPC connections, DB clients, message producer handles
- **Goroutine management**: Bounded concurrency with semaphores — don't spawn unbounded goroutines
- **Memory**: Prefer pre-allocated slices, avoid excessive allocations in hot paths
- **Context timeouts**: Set deadlines on all external calls (DB, gRPC, message broker)

### Message Brokers
- **Consumer tuning**: Batch size, fetch size, and poll interval affect throughput vs. latency
- **Partition count**: More partitions = more parallelism, but more overhead — match to consumer count
- **Consumer lag monitoring**: Alert before lag becomes a business problem

### Caching (where applicable)
- **CDN**: CDN caching for public-facing API responses
- **Application-level**: In-memory caches for reference data (products, accounts) with TTL
- **Query result caching**: Many analytics stores cache identical queries — leverage by standardizing query patterns

---

## Infrastructure as Code (IaC) Patterns

### Structural Patterns
- **Module composition**: Small, single-purpose modules composed together (like Composite pattern)
- **Variable abstraction**: Expose only what consumers need (like Facade pattern)
- **Provider configuration**: Centralize provider config in root, not in modules (DRY)

### Anti-Patterns in IaC
| Anti-Pattern | Symptoms | Fix |
|---|---|---|
| God Module | One module managing network + cluster + IAM + DNS | Split by resource domain |
| Hardcoded values | Magic numbers, inline project IDs | Use variables and locals |
| State sprawl | One giant state file for everything | State per environment x business unit |
| Copy-paste environments | Identical .tf files per stage | IaC wrapper with DRY includes |
| Missing outputs | Modules that don't expose what dependents need | Define outputs for every cross-module reference |

---

## Container Best Practices

> Applies to both Go and Python containers.

### Multi-Stage Builds
- **Go**: build stage with `golang:<version>-alpine`, final stage from `distroless/static-debian12:nonroot` — copy only the static binary
- **Python**: base stage installs system deps, dependency stage installs pip packages, production stage copies only installed packages and app code
- Copy dependency files (`go.mod`/`go.sum`, `requirements.txt`) before source code to maximize Docker layer caching

### Security Hardening
- **Non-root user**: always create and switch to a non-root user (`USER appuser`) — container security standards enforce this
- **Read-only filesystem**: set `readOnlyRootFilesystem: true` in security context; mount writable tmpfs only where needed
- **No package managers in prod**: remove or don't install `apt`/`apk`/`pip` in the final image — reduces attack surface
- **Pin base image digests**: use `image@sha256:...` in production Dockerfiles, not just tags — tags are mutable

### Image Scanning & .dockerignore
- **Trivy scan in CI**: scan images for HIGH/CRITICAL CVEs before pushing — block merge on critical findings
- **.dockerignore**: exclude `.git/`, `*.md`, `test/`, `docs/`, IDE configs, and local env files — keeps build context small and avoids leaking secrets
- **Image size budget**: Go services should target <50MB (scratch-based), Python services <200MB (slim-based)

### Health Checks & Signals
- **HEALTHCHECK**: define in Dockerfile; liveness/readiness probes should match
- **Graceful shutdown**: handle `SIGTERM` properly — drain in-flight requests, close DB/broker connections, then exit
- **Use `dumb-init` or `tini`** for Python containers to ensure proper signal forwarding (Go binaries handle signals natively)

---

## Pattern Implementation Checklist

Before implementing any pattern:
- [ ] Problem clearly identified — what specific issue does this solve?
- [ ] Simpler alternatives considered — could a plain function solve this?
- [ ] Team familiarity assessed — will others understand this code?
- [ ] Future maintenance considered — does this make changes easier or harder?

After implementation:
- [ ] Rationale documented (ADR if significant)
- [ ] Tests written covering the pattern's behavior
- [ ] No performance regression introduced

---

## Cross-References

- See `rules/architectural-decision-records.md` for when and how to document pattern choices as ADRs
- See `rules/project-planning.md` for planning frameworks that guide architectural decisions
