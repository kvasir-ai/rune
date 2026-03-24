---
name: release
description: Prepare a release — validate state, update CHANGELOG, bump version, commit, and tag. Use when ready to cut a new version.
argument-hint: <version> (e.g., 0.2.0)
---

# Release

Prepare and cut a release. Validates the repo is clean, updates version references, and creates a signed tag.

**Announce at start:** "Preparing release. Checking preconditions."

## Step 1: Parse Version

Extract the target version from `$ARGUMENTS`. Must be valid semver (e.g., `0.2.0`, `1.0.0`).

If no version is provided, read the current version from `pyproject.toml` and suggest the next patch, minor, or major bump. Ask the user which one.

## Step 2: Precondition Checks

Run all checks. If any fail, stop and report.

```bash
# 1. No uncommitted changes (except CHANGELOG.md which we're about to update)
git status --porcelain | grep -v CHANGELOG.md

# 2. On main branch
git branch --show-current

# 3. Up to date with remote
git fetch origin && git diff origin/main..HEAD --stat

# 4. Validation passes
make validate
```

**If uncommitted changes exist:**
- Show them
- Ask: "Commit these changes first, or abort release?"
- If commit: stage all, commit with message "Pre-release cleanup", then continue
- If abort: stop

**If not on main:** warn but don't block — some workflows release from feature branches.

## Step 3: Update CHANGELOG

Read `CHANGELOG.md`. Find the `## [Unreleased]` section.

- If there is content under `[Unreleased]`, move it into a new version section with today's date
- If `[Unreleased]` is empty, read `git log` since the last tag and summarize changes into Added/Changed/Removed sections
- Keep entries concise — one line per change, no prose

**Format:**

```markdown
## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

### Added
- New feature or file

### Changed
- Modified behavior or config

### Removed
- Deleted feature or file
```

Show the proposed CHANGELOG diff to the user before writing.

## Step 4: Bump Version

Update the version string in these files (if they exist):

| File | Field |
|---|---|
| `pyproject.toml` | `version = "X.Y.Z"` |
| `package.json` | `"version": "X.Y.Z"` |

Search for other version references:
```bash
grep -rn "0\.1\.0" --include="*.toml" --include="*.json" --include="*.yaml" . | grep -v node_modules | grep -v .git
```

Show all matches. Update the ones that are product version references. Skip dependency version pins.

## Step 5: Commit

Stage all changes and commit:

```
Release vX.Y.Z
```

Do not add any co-author attribution.

## Step 6: Tag

Create a signed annotated tag:

```bash
git tag -s vX.Y.Z -m "rune vX.Y.Z"
```

If GPG signing fails, create an unsigned annotated tag and warn:

```bash
git tag -a vX.Y.Z -m "rune vX.Y.Z"
```

## Step 7: Summary

```
───────────────────────────────────────────
  RELEASE PREPARED
───────────────────────────────────────────

  Version:    vX.Y.Z
  Tag:        vX.Y.Z (signed)
  Commit:     abc1234
  CHANGELOG:  Updated with N entries
  Files:      pyproject.toml bumped

  Push with:
    git push origin main --tags

───────────────────────────────────────────
```

Do NOT push automatically. The user decides when to push.

## Rules

1. **Never push.** Prepare the release locally. The user pushes.
2. **Never skip validation.** `make validate` must pass.
3. **Show before writing.** Display the CHANGELOG diff before committing.
4. **Semver only.** Reject non-semver version strings.
5. **Tag matches version.** Tag is always `vX.Y.Z` (with `v` prefix).
