#!/usr/bin/env python3
"""
Safety-check hook test suite.

Validates that safety-patterns.yaml + safety-check.py correctly block
destructive commands, pass safe commands, catch evasion attempts, and
documents known bypasses.

Run: python3 tests/test-safety-check.py
"""

import sys
from pathlib import Path

# Import from the actual hook code instead of reimplementing
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src" / "hooks"))

from importlib import import_module

# safety-check.py has a hyphen, so we cannot use a normal import statement
safety_check = import_module("safety-check")

load_patterns = safety_check.load_patterns
is_rm_recursive_force = safety_check.is_rm_recursive_force
check_pattern = safety_check.check_pattern


def check(cmd: str, patterns: list[dict]) -> str | None:
    """Thin wrapper: run all patterns against a command, return the matched name or None.

    Mirrors the hook's main() logic but returns the pattern name for test assertions.
    Only 'block' severity counts as a block -- 'warn' patterns do not block.
    """
    for p in patterns:
        result = check_pattern(p, cmd)
        if result:
            _message, severity = result
            if severity == "block":
                return p.get("name")
    return None


def check_any(cmd: str, patterns: list[dict]) -> tuple[str, str] | None:
    """Return (name, severity) for the first matching pattern regardless of severity."""
    for p in patterns:
        result = check_pattern(p, cmd)
        if result:
            _message, severity = result
            return (p.get("name", ""), severity)
    return None


def main():
    patterns = load_patterns()
    failures = 0

    # -- Commands that MUST be blocked ----------------------------------------

    block_cases = [
        # rm recursive+force (all flag variations)
        ("rm -rf /", "rm-recursive-force"),
        ("rm -fr /tmp/data", "rm-recursive-force"),
        ("rm -r -f .", "rm-recursive-force"),
        ("rm --recursive --force /var", "rm-recursive-force"),
        ("rm -Rf /home", "rm-recursive-force"),
        ("rm -rfv /data", "rm-recursive-force"),
        ("ls && rm -rf /tmp", "rm-recursive-force"),

        # SQL destructive operations
        ("DROP TABLE users", "drop-table"),
        ("drop table users", "drop-table"),
        ("DROP DATABASE mydb", "drop-database"),
        ("DELETE FROM orders", "delete-from"),
        ("TRUNCATE payments", "truncate"),

        # Destructive git
        ("git push --force", "git-force-push"),
        ("git push -f origin main", "git-force-push"),
        ("git reset --hard", "git-reset-hard"),
        ("git clean -fd", "git-clean"),
        ("git checkout .", "git-checkout-dot"),
        ("git restore .", "git-restore-dot"),
        ("git branch -D feature", "git-branch-force-delete"),

        # Infrastructure
        ("terraform apply -var-file=prod.tfvars", "terraform-production-apply"),
        ("terragrunt apply --target production", "terraform-production-apply"),
        ("terraform apply -target=live", "terraform-production-apply"),
        ("terraform destroy", "terraform-destroy"),
        ("terraform destroy -auto-approve", "terraform-destroy"),
        ("terragrunt destroy", "terraform-destroy"),

        # Shell indirection
        ("bash -c 'rm -rf /tmp'", "bash-c-destructive"),
        ("sh -c \"rm -rf /var/data\"", "bash-c-destructive"),
        ("eval 'rm -rf /tmp/stuff'", "eval-destructive"),

        # Authentication
        ("gcloud auth login", "gcloud-auth"),
        ("gcloud auth application-default login", "gcloud-auth"),
        ("gh auth login", "gh-auth"),
    ]

    print("=== MUST BLOCK (destructive commands) ===\n")
    for cmd, expected in block_cases:
        result = check(cmd, patterns)
        if result:
            print(f"  PASS  {cmd:<55} blocked by: {result}")
        else:
            print(f"  FAIL  {cmd:<55} NOT BLOCKED (expected: {expected})")
            failures += 1

    # -- Commands that MUST pass through --------------------------------------

    pass_cases = [
        ("ls -la", "safe listing"),
        ("rm file.txt", "single file delete (no recursive)"),
        ("rm -r /tmp/safe", "recursive without force"),
        ("rm -f single-file", "force without recursive"),
        ("git push origin main", "normal push"),
        ("git push --force-with-lease", "safe force alternative"),
        ("git reset --soft HEAD~1", "soft reset"),
        ("git clean -n", "dry run clean"),
        ("git checkout feature", "branch checkout"),
        ("git restore --staged .", "unstage files"),
        ("git branch -d feature", "safe branch delete (lowercase d)"),
        ("terraform plan", "plan only"),
        ("terraform apply -var-file=dev.tfvars", "non-production apply"),
        ("SELECT * FROM users", "read-only SQL"),
        ("gcloud compute list", "non-auth gcloud"),
        ("gcloud auth revoke", "auth revoke is safe (not login)"),
        ("gh repo view", "non-auth gh"),
    ]

    print("\n=== MUST PASS (safe commands) ===\n")
    for cmd, description in pass_cases:
        result = check(cmd, patterns)
        if not result:
            print(f"  PASS  {cmd:<55} ({description})")
        else:
            print(f"  FAIL  {cmd:<55} FALSE POSITIVE: blocked by {result}")
            failures += 1

    # -- Evasion attempts that MUST be caught ---------------------------------

    evasion_cases = [
        ("rm    -rf   /", "rm-recursive-force", "extra whitespace"),
        ("rm -r -v -f /data", "rm-recursive-force", "flags split with others"),
        ("; rm -rf /", "rm-recursive-force", "after semicolon"),
        ("echo hi && rm -rf /tmp", "rm-recursive-force", "after &&"),
        ("echo hi | rm -rf /tmp", "rm-recursive-force", "after pipe"),
        ("DROP   TABLE   users", "drop-table", "extra whitespace in SQL"),
        ("  git push --force  ", "git-force-push", "leading/trailing spaces"),
    ]

    print("\n=== EVASION ATTEMPTS (must catch) ===\n")
    for cmd, expected, technique in evasion_cases:
        result = check(cmd, patterns)
        if result:
            print(f"  PASS  {cmd:<55} caught ({technique})")
        else:
            print(f"  FAIL  {cmd:<55} EVADED ({technique})")
            failures += 1

    # -- Severity:warn behavior (must NOT block) ------------------------------

    # To test warn behavior, we temporarily add a warn-severity pattern
    warn_pattern = {
        "name": "test-warn-pattern",
        "match": r"\bwarn-test-command\b",
        "message": "This is a warning, not a block",
        "severity": "warn",
    }
    test_patterns_with_warn = patterns + [warn_pattern]

    warn_cases = [
        ("warn-test-command --flag", "test-warn-pattern", "warn severity must not block"),
    ]

    print("\n=== SEVERITY:WARN (must NOT block, must match) ===\n")
    for cmd, expected_name, description in warn_cases:
        # check() only returns blocks -- should return None for warn
        block_result = check(cmd, test_patterns_with_warn)
        # check_any() returns any match -- should return the warn pattern
        any_result = check_any(cmd, test_patterns_with_warn)

        if block_result is None and any_result is not None:
            name, severity = any_result
            if name == expected_name and severity == "warn":
                print(f"  PASS  {cmd:<55} matched as warn, not blocked ({description})")
            else:
                print(f"  FAIL  {cmd:<55} wrong match: {name}/{severity} (expected: {expected_name}/warn)")
                failures += 1
        elif block_result is not None:
            print(f"  FAIL  {cmd:<55} BLOCKED (warn should not block) ({description})")
            failures += 1
        else:
            print(f"  FAIL  {cmd:<55} NOT MATCHED at all (expected warn match) ({description})")
            failures += 1

    # -- Known bypasses (documented, not failures) ----------------------------

    bypass_cases = [
        ("find / -delete", "alternative deletion command"),
        ("perl -e 'unlink glob(\"*\")'", "scripting language bypass"),
        ("python3 -c 'import shutil; shutil.rmtree(\"/\")'", "python bypass"),
        ("cat /dev/null > important_file", "redirection data destruction"),
        ("dd if=/dev/zero of=/dev/sda", "disk wipe via dd"),
        ("chmod -R 000 /", "permission destruction"),
        ("git push origin :main", "colon syntax remote branch delete"),
    ]

    print("\n=== KNOWN BYPASSES (documented, not failures) ===\n")
    for cmd, description in bypass_cases:
        result = check(cmd, patterns)
        if not result:
            print(f"  INFO  {cmd:<55} not caught ({description})")
        else:
            print(f"  INFO  {cmd:<55} caught by {result} ({description})")

    # -- Summary --------------------------------------------------------------

    total = len(block_cases) + len(pass_cases) + len(evasion_cases) + len(warn_cases)
    passed = total - failures

    print(f"\n{'='*60}")
    print(f"  Patterns loaded:  {len(patterns)}")
    print(f"  Tests run:        {total}")
    print(f"  Passed:           {passed}")
    print(f"  Failed:           {failures}")
    print(f"  Known bypasses:   {len(bypass_cases)} (documented)")
    print(f"  Result:           {'PASS' if failures == 0 else 'FAIL'}")
    print(f"{'='*60}")

    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
