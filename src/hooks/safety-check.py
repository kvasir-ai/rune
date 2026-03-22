#!/usr/bin/env python3
"""
PreToolUse hook: block dangerous commands

Prevents execution of destructive operations like:
- rm with recursive+force flags (any flag ordering or long-form)
- DROP TABLE, DELETE FROM, TRUNCATE
- Destructive git commands (force push, hard reset, clean -f, etc.)
- terraform/terragrunt apply to production (live/sandbox/production/prod)
- Authentication attempts (gcloud auth, gh auth)
"""

import json
import sys
import re


def read_json_input() -> dict:
    """Read and parse JSON from stdin."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return {}


def get_command(data: dict) -> str:
    """Extract the bash command being executed."""
    return data.get("tool_input", {}).get("command", "")


def make_deny_response(reason: str) -> dict:
    """Create a denial response JSON."""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def is_rm_recursive_force(cmd: str) -> bool:
    """Check if a command is 'rm' with both recursive and force flags.

    Catches all variations:
    - rm -rf, rm -fr, rm -rfv, rm -r -f, rm -Rf
    - rm --recursive --force, rm --recursive -f, rm -r --force
    - rm with any interleaved flags like rm -r -v -f

    The logic: if the command starts with 'rm' (as a word) and contains
    BOTH a recursive flag AND a force flag anywhere, block it.
    """
    # Iterate over ALL rm invocations in the command (handles compound commands)
    for rm_match in re.finditer(r"(?:^|[;&|]\s*)\brm\b([^;&|]*)", cmd):
        flags = rm_match.group(1)

        # Check for recursive flag: -r, -R, --recursive, or bundled like -rf, -Rf, -rfv
        has_recursive = bool(
            re.search(r"--recursive\b", flags)
            or re.search(r"-[a-zA-Z]*[rR]", flags)
        )

        # Check for force flag: -f, --force, or bundled like -rf, -fr, -fv
        has_force = bool(
            re.search(r"--force\b", flags)
            or re.search(r"-[a-zA-Z]*f", flags)
        )

        if has_recursive and has_force:
            return True

    return False


def check_destructive_commands(cmd: str) -> str | None:
    """Check for destructive bash/SQL commands."""
    # C1: Comprehensive rm recursive+force detection
    if is_rm_recursive_force(cmd):
        return "Destructive command blocked: rm with recursive+force. Use targeted operations instead."

    # SQL destructive operations
    sql_patterns = [
        (
            r"\bDROP\s+TABLE\b",
            "Destructive command blocked: DROP TABLE. Use targeted operations instead.",
        ),
        (
            r"\bDROP\s+DATABASE\b",
            "Destructive command blocked: DROP DATABASE. Use targeted operations instead.",
        ),
        (
            r"\bDELETE\s+FROM\b",
            "Destructive command blocked: DELETE FROM. Use targeted operations instead.",
        ),
        (
            r"\bTRUNCATE\b",
            "Destructive command blocked: TRUNCATE. Use targeted operations instead.",
        ),
    ]

    for pattern, reason in sql_patterns:
        if re.search(pattern, cmd, re.IGNORECASE):
            return reason

    return None


def check_destructive_git(cmd: str) -> str | None:
    """Check for destructive git commands.

    Blocks:
    - git push --force / -f (but NOT --force-with-lease, which is safer)
    - git reset --hard
    - git clean -f / -fd
    - git checkout . (discard all uncommitted changes)
    - git restore . (discard all uncommitted changes)
    - git branch -D (force delete branch)
    """
    patterns = [
        # git push --force or -f, but not --force-with-lease
        # Negative lookahead ensures --force-with-lease is allowed
        (
            r"\bgit\s+push\b.*(?:--force(?!-with-lease)\b|-(?=[a-zA-Z]*f)[a-zA-Z]*f\b)",
            "Destructive git command blocked: force push. Use --force-with-lease if needed.",
        ),
        # git reset --hard
        (
            r"\bgit\s+reset\s+--hard\b",
            "Destructive git command blocked: hard reset discards uncommitted changes.",
        ),
        # git clean with -f flag (possibly combined: -fd, -fx, -fxd, etc.)
        (
            r"\bgit\s+clean\b.*-[a-zA-Z]*f",
            "Destructive git command blocked: git clean -f removes untracked files.",
        ),
        # git checkout . (discard all changes in working tree)
        (
            r"\bgit\s+checkout\s+\.",
            "Destructive git command blocked: git checkout . discards all uncommitted changes.",
        ),
        # git restore . (discard all changes in working tree)
        (
            r"\bgit\s+restore\s+\.",
            "Destructive git command blocked: git restore . discards all uncommitted changes.",
        ),
        # git branch -D (force delete, case-sensitive D)
        (
            r"\bgit\s+branch\s+-D\b",
            "Destructive git command blocked: git branch -D force-deletes a branch.",
        ),
    ]

    for pattern, reason in patterns:
        if re.search(pattern, cmd):
            return reason

    return None


def check_production_apply(cmd: str) -> str | None:
    """Check for terraform/terragrunt apply to production.

    M4: Includes 'prod' as a production keyword alongside live/sandbox/production.
    """
    has_apply = bool(
        re.search(r"(terragrunt|terraform)\s+apply", cmd, re.IGNORECASE)
    )
    has_prod = bool(
        re.search(r"(live|sandbox|production|prod)", cmd, re.IGNORECASE)
    )

    if has_apply and has_prod:
        return "Production apply blocked. CI/CD is the only path to production."

    return None


def check_auth_attempts(cmd: str) -> str | None:
    """Check for authentication command attempts.

    Blocks any gcloud auth sub-command (login, application-default login,
    activate-service-account, etc.) and any gh auth sub-command.
    """
    patterns = [
        r"\bgcloud\s+auth\b",
        r"\bgh\s+auth\b",
    ]

    for pattern in patterns:
        if re.search(pattern, cmd, re.IGNORECASE):
            return "Authentication blocked. Ask the user to authenticate manually."

    return None


def main():
    data = read_json_input()
    cmd = get_command(data)

    if not cmd:
        sys.exit(0)

    # Check in order: destructive commands, destructive git, production apply, auth
    reason = (
        check_destructive_commands(cmd)
        or check_destructive_git(cmd)
        or check_production_apply(cmd)
        or check_auth_attempts(cmd)
    )

    if reason:
        response = make_deny_response(reason)
        print(json.dumps(response))
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
