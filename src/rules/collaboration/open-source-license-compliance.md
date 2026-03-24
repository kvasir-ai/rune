# Open Source License Compliance

> License obligations for contributors and users of open source projects.
> Covers MIT, Apache 2.0, GPL family, and dependency scanning.
> Every agent must follow these constraints when adding dependencies or generating code.

---

## License Compatibility

### Permissive Licenses (safe to use and combine)

| License | Attribution Required | Copyleft | Commercial Use | Notes |
|---|---|---|---|---|
| MIT | Yes (preserve notice) | No | Yes | Most common. Include LICENSE file. |
| Apache 2.0 | Yes (preserve notice + NOTICE file) | No | Yes | Includes patent grant. |
| BSD-2-Clause | Yes (preserve notice) | No | Yes | Minimal obligations. |
| BSD-3-Clause | Yes (preserve notice) | No | Yes | Adds non-endorsement clause. |
| ISC | Yes (preserve notice) | No | Yes | Functionally identical to MIT. |
| CC0 / Unlicense | No | No | Yes | Public domain equivalent. |

### Copyleft Licenses (restrictions on distribution)

| License | Scope | Obligation | Risk |
|---|---|---|---|
| GPL-2.0 | Strong copyleft | Derivative works must be GPL-2.0 | Viral — contaminates linked code |
| GPL-3.0 | Strong copyleft | Same as GPL-2.0 + anti-tivoization | Same risk, stricter terms |
| LGPL-2.1 / LGPL-3.0 | Weak copyleft | Library can be used without copyleft if dynamically linked | Safe for CLI tools and libraries used at arm's length |
| MPL-2.0 | File-level copyleft | Modified MPL files must stay MPL; other files can be any license | Safe for most uses — copyleft is per-file, not per-project |
| AGPL-3.0 | Network copyleft | Server-side use triggers copyleft (not just distribution) | Avoid in SaaS — triggers on network interaction |

### License Combinations

| Your Project License | Can Depend On |
|---|---|
| MIT | MIT, BSD, ISC, Apache 2.0, CC0, Unlicense |
| Apache 2.0 | MIT, BSD, ISC, Apache 2.0, CC0, Unlicense |
| GPL-3.0 | Anything (GPL absorbs) |
| MIT | **Cannot** depend on GPL (GPL would require your project to become GPL) |

---

## Rules for Contributors

### Adding Dependencies

1. **Check the license before adding any dependency.** Run `license-checker`, `cargo license`, `pip-licenses`, or equivalent for your language.
2. **No GPL dependencies in MIT/Apache projects** unless isolated by process boundary (separate binary, separate container).
3. **No AGPL dependencies** in any project that runs as a service.
4. **LGPL is acceptable** for dynamically linked libraries and CLI tools used as external processes.
5. **MPL-2.0 is acceptable** — file-level copyleft does not contaminate the rest of the project.

### Writing Code

1. **Do not copy code from Stack Overflow, GitHub, or AI output without checking its license.** Unlicensed code defaults to "all rights reserved" in most jurisdictions.
2. **AI-generated code has no copyright holder** in most jurisdictions. Treat it as if it were public domain for licensing purposes, but review for inadvertent reproduction of licensed code.
3. **When in doubt, rewrite from scratch** rather than copying. Clean-room implementation avoids license contamination.

### Attribution

1. **Preserve all LICENSE and NOTICE files** from dependencies.
2. **Include copyright headers** in source files when the project convention requires it.
3. **Credit upstream projects** in your project's LICENSE or THIRD-PARTY-NOTICES file.

---

## Dependency Scanning

Run license checks in CI before merging:

| Language | Tool | Command |
|---|---|---|
| Python | `pip-licenses` | `pip-licenses --format=table --fail-on="GPL-2.0;GPL-3.0;AGPL-3.0"` |
| Go | `go-licenses` | `go-licenses check ./...` |
| Node.js | `license-checker` | `npx license-checker --failOn "GPL-2.0;GPL-3.0;AGPL-3.0"` |
| Rust | `cargo-license` | `cargo license --avoid "GPL-2.0 GPL-3.0 AGPL-3.0"` |

Block merges when a disallowed license is detected.

---

## Cross-References

- See `rules/operational-constraints.md` for production safety and general agent constraints
