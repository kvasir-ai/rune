#!/usr/bin/env python3
"""
PostToolUse hook: auto-lint after file writes

Detects file type and runs the appropriate linter:
- Python: ruff check + ruff format
- SQL: sqlfluff fix (if in dbt project)
- Go: goimports
- Terraform: terraform fmt
"""

import json
import os
import sys
import subprocess
from pathlib import Path


def read_json_input() -> dict:
    """Read and parse JSON from stdin."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return {}


def get_file_path(data: dict) -> str:
    """Extract the file path from hook input."""
    return data.get("tool_input", {}).get("file_path", "")


def lint_python(file_path: str):
    """Lint Python file with ruff."""
    try:
        subprocess.run(
            ["ruff", "check", "--fix", file_path], capture_output=True, timeout=10
        )
        subprocess.run(["ruff", "format", file_path], capture_output=True, timeout=10)
    except FileNotFoundError:
        pass
    except subprocess.TimeoutExpired:
        print(f"Warning: ruff timed out on {file_path}", file=sys.stderr)


def lint_sql(file_path: str):
    """Lint SQL file with sqlfluff (if in dbt project)."""
    # Only run if dbt/dbt_project.yml exists
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.cwd()))
    dbt_project = project_dir / "dbt" / "dbt_project.yml"
    if not dbt_project.is_file():
        return

    try:
        subprocess.run(
            ["sqlfluff", "fix", "--force", file_path],
            cwd=project_dir / "dbt",
            capture_output=True,
            timeout=10,
        )
    except FileNotFoundError:
        pass
    except subprocess.TimeoutExpired:
        print(f"Warning: sqlfluff timed out on {file_path}", file=sys.stderr)


def lint_go(file_path: str):
    """Lint Go file with goimports."""
    try:
        subprocess.run(["goimports", "-w", file_path], capture_output=True, timeout=10)
    except FileNotFoundError:
        pass
    except subprocess.TimeoutExpired:
        print(f"Warning: goimports timed out on {file_path}", file=sys.stderr)


def lint_terraform(file_path: str):
    """Format Terraform file."""
    try:
        subprocess.run(["terraform", "fmt", file_path], capture_output=True, timeout=10)
    except FileNotFoundError:
        pass
    except subprocess.TimeoutExpired:
        print(f"Warning: terraform timed out on {file_path}", file=sys.stderr)


def lint_file(file_path: str):
    """Dispatch to appropriate linter based on file extension."""
    if not file_path or not Path(file_path).is_file():
        return

    ext = Path(file_path).suffix.lstrip(".")

    linters = {
        "py": lint_python,
        "sql": lint_sql,
        "go": lint_go,
        "tf": lint_terraform,
    }

    if ext in linters:
        linters[ext](file_path)


def main():
    data = read_json_input()
    file_path = get_file_path(data)
    lint_file(file_path)


if __name__ == "__main__":
    main()
