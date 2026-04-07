---
phase: validate
description: Prepare a release — validate state, generate release notes, update CHANGELOG, bump version, commit, and tag. Use when ready to cut a new version.
argument-hint: <version> (e.g., 0.2.0)
user_invocable: true
---

# Release

Shared contract: apply `.claude/skills/core/skill-contract/SKILL.md`
before following the phase-specific steps below.

Prepare and cut a release. Validates the repo is clean, generates release notes, updates version references, and creates a tag.

**Announce at start:** "Preparing release. Checking preconditions."

## Step 1: Parse Version

Extract the target version from `$ARGUMENTS`. Must be valid semver (e.g., `0.2.0`, `1.0.0`).

If no version is provided, read the current version from `pyproject.toml` or `package.json` and suggest the next patch, minor, or major bump. Ask the user which one.

## Step 2: Precondition Checks

Run all checks. If any fail, stop and report.

```bash
# 1. No uncommitted changes (except CHANGELOG.md which we're about to update)
git status --porcelain | grep -v CHANGELOG.md

# 2. On main branch (warn but don't block if not)
git branch --show-current

# 3. Up to date with remote
git fetch origin && git diff origin/main..HEAD --stat

# 4. Project validation passes
rune system validate
```

## Step 3: Generate Release Notes

Read `git log` since the last tag and generate release notes:

```bash
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -n "$LAST_TAG" ]; then
  git log --oneline "$LAST_TAG..HEAD"
else
  git log --oneline HEAD~20..HEAD
fi
```

Group changes by category:
- **Features** — new capabilities
- **Fixes** — bug fixes
- **Infrastructure** — build, CI, config changes
- **Documentation** — doc updates

Extract ticket references (`grep -oE '[A-Z]+-[0-9]+'`) and group by ticket where possible.

## Step 4: Update CHANGELOG

Read `CHANGELOG.md`. Find the `## [Unreleased]` section.

- If there is content under `[Unreleased]`, move it into a new version section with today's date
- If `[Unreleased]` is empty, use the generated release notes from Step 3

### Release Notes Template

Use this section shape when generating or moving release notes:

```markdown
## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

### Added
- "<new capability>"

### Changed
- "<behavior or process change>"

### Removed
- "<removal>"
```

Show the proposed CHANGELOG diff to the user before writing.

## Step 5: Bump Version

Update the version string in these files (if they exist):

| File | Field |
|---|---|
| `pyproject.toml` | `version = "X.Y.Z"` |
| `package.json` | `"version": "X.Y.Z"` |

Search for other version references and show matches. Update product version references. Skip dependency version pins.

## Step 6: Commit and Tag

Stage all changes and commit:

```bash
git add -A
git commit -m "Release vX.Y.Z"
```

Create an annotated tag:

```bash
git tag -a vX.Y.Z -m "vX.Y.Z"
```

If GPG signing is configured, use signed tag (`git tag -s`).

## Step 7: Summary

Use this exact release summary frame:

```text
-------------------------------------------
  RELEASE PREPARED
-------------------------------------------

  Version:    vX.Y.Z
  Tag:        vX.Y.Z
  Commit:     abc1234
  CHANGELOG:  Updated
  Files:      [list of bumped files]

  Push with:
    git push origin main --tags

-------------------------------------------
```

Do NOT push automatically. The user decides when to push.

## Output Rules

1. **Never push.** Prepare the release locally. The user pushes.
2. **Never skip validation.** Precondition checks must pass.
3. **Show before writing.** Display the CHANGELOG diff before committing.
4. **Semver only.** Reject non-semver version strings.
5. **Tag matches version.** Tag is always `vX.Y.Z` (with `v` prefix).
6. **List bumped files.** The final summary must say which files had version updates.
7. **Stop on failed preconditions.** Do not continue optimistically after a failing check.
