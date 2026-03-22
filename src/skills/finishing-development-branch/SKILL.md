---
name: finishing-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work. Guides completion by presenting structured options for merge, PR, or cleanup.
---

# Finishing a Development Branch

Guide completion of development work by presenting clear options and handling the chosen workflow.

**Core principle:** Verify tests → Present options → Execute choice → Clean up.

## The Process

### Step 1: Verify Tests

```bash
# Run the project's test suite
npm test / cargo test / pytest / go test ./...
```

If tests fail: stop. Don't proceed until they pass.

### Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

### Step 3: Present Options

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

### Step 4: Execute Choice

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|---|---|---|---|---|
| 1. Merge locally | Yes | — | — | Yes |
| 2. Create PR | — | Yes | Yes | — |
| 3. Keep as-is | — | — | Yes | — |
| 4. Discard | — | — | — | Yes (force) |

**Option 4 requires typed confirmation** — never delete work without explicit consent.

### Step 5: Cleanup Worktree

For Options 1 and 4, remove the worktree if one was created:
```bash
git worktree remove <worktree-path>
```

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on result
- Delete work without confirmation
- Force-push without explicit request

## Integration

- **subagent-driven-development** — called after all tasks complete
- **executing-plans** — called after all batches complete
- **pr-description** — generates PR description for Option 2
