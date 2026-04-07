"""Core integration tests for the rune agent system."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from importlib import import_module
from pathlib import Path
from typing import Any

import pytest
from click.testing import CliRunner

ROOT = Path(__file__).resolve().parent.parent
HOOKS_ROOT = ROOT / "src" / "rune-agency" / "hooks"
HOOKS_DIR = HOOKS_ROOT / "core"
SRC_DIR = ROOT / "src"
SKILLS_DIR = ROOT / "src" / "rune-agency" / "skills"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Import safety-check hook
if str(HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(HOOKS_DIR))
safety_check = import_module("safety-check")


def _hook_path(name: str) -> Path:
    matches = sorted(HOOKS_ROOT.rglob(f"{name}.py"))
    assert len(matches) == 1, name
    return matches[0]


def run_hook(name: str, project_dir: Path, payload: dict | None = None) -> str:
    """Helper to run a workflow hook from CLI."""
    hook_path = _hook_path(name)
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    env["CLAUDE_PROJECT_DIR"] = str(project_dir)
    result = subprocess.run(
        [sys.executable, str(hook_path)],
        input=json.dumps(payload or {}),
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    return result.stdout.strip()


def test_safety_hooks() -> None:
    """Verify safety hook blocks destructive commands and allows safe ones."""
    patterns = safety_check.load_patterns()
    cases = [
        ("rm -rf /", True),
        ("DROP TABLE users", True),
        ("git push --force", True),
        ("terraform destroy", True),
        ("bash -c 'rm -rf /tmp'", True),
        ("ls -la", False),
        ("rm file.txt", False),
        ("git push origin main", False),
        ("terraform plan", False),
        ("SELECT * FROM users", False),
    ]

    for cmd, expected_blocked in cases:
        blocked = False
        for p in patterns:
            result = safety_check.check_pattern(p, cmd)
            if result:
                _, severity = result
                if severity == "block":
                    blocked = True
                    break
        assert blocked == expected_blocked, (
            f"Command '{cmd}' expected_blocked={expected_blocked}, got={blocked}"
        )


def test_configure_profile_deploys_all_resource_types(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from cli import settings
    from cli.commands.deploy import configure_profile

    src = tmp_path / "agency"
    claude_dir = tmp_path / ".claude"
    claude_src = tmp_path / "platform"

    for directory in (
        src / "agents" / "core",
        src / "rules" / "build",
        src / "skills" / "shell-tooling",
        src / "hooks" / "core",
        claude_src / "agents",
    ):
        directory.mkdir(parents=True, exist_ok=True)

    (src / "agents" / "core" / "planner.md").write_text("---\nname: planner\n---\n")
    (src / "rules" / "build" / "python-cleanup.md").write_text("# cleanup\n")
    (src / "skills" / "shell-tooling" / "SKILL.md").write_text("---\nname: shell-tooling\n---\n")
    (src / "hooks" / "core" / "safety-check.py").write_text("print('ok')\n")
    (src / "hooks" / "core" / "safety-patterns.yaml").write_text("patterns: []\n")
    (src / "hooks-meta.yaml").write_text(
        """\
core/safety-check:
  events:
    PreToolUse:
      matcher: Bash
      timeout: 5
""",
        encoding="utf-8",
    )
    (src / "mcps.yaml").write_text(
        """\
demo:
  claude:
    command: demo-mcp
    args: ["serve"]
""",
        encoding="utf-8",
    )
    (claude_src / "agents" / "platform-helper.md").write_text("---\nname: helper\n---\n")
    (claude_src / "settings.json").write_text(
        json.dumps({"model": "sonnet", "permissions": {"allow": ["Bash"]}}),
        encoding="utf-8",
    )
    (claude_src / "statusline_command.py").write_text("print('status')\n")
    (claude_src / "statusline.yaml").write_text("enabled: true\n")

    monkeypatch.setattr(settings, "CLAUDE_DIR", claude_dir)

    profile = {
        "agents": {"core": ["core/planner"]},
        "rules": {"build": ["build/python-cleanup"]},
        "skills": ["shell-tooling"],
        "hooks": ["core/safety-check"],
        "mcps": ["demo"],
    }

    configure_profile(profile, "claude", tmp_path, src, claude_dir, claude_src)

    assert (claude_dir / "agents" / "planner.md").exists()
    assert (claude_dir / "agents" / "platform-helper.md").exists()
    assert (claude_dir / "rules" / "python-cleanup.md").exists()
    assert (claude_dir / "skills" / "shell-tooling" / "SKILL.md").exists()
    assert (claude_dir / "hooks" / "safety-check.py").exists()
    assert (claude_dir / "hooks" / "safety-patterns.yaml").exists()
    assert (claude_dir / "statusline_command.py").exists()
    assert (claude_dir / "statusline.yaml").exists()

    settings_json = json.loads((claude_dir / "settings.json").read_text())
    assert settings_json["model"] == "sonnet"
    assert settings_json["permissions"] == {"allow": ["Bash"]}
    assert settings_json["statusLine"]["command"] == f"python3 {claude_dir / 'statusline_command.py'}"
    assert settings_json["hooks"]["PreToolUse"][0]["matcher"] == "Bash"
    assert settings_json["hooks"]["PreToolUse"][0]["hooks"][0]["command"] == (
        f"{claude_dir / 'hooks' / 'safety-check.py'}"
    )
    assert settings_json["mcpServers"]["demo"]["command"] == "demo-mcp"


def test_apply_tracks_hook_state_with_deployed_short_names(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from cli import settings, setup_core
    from cli._common import load_managed_state

    monkeypatch.chdir(tmp_path)

    agency = tmp_path / "agency"
    claude_src = tmp_path / "platform"
    install_dir = tmp_path / ".claude"

    for directory in (
        agency / "agents" / "core",
        agency / "rules" / "build",
        agency / "hooks" / "core",
        claude_src,
        install_dir,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    (agency / "agents" / "core" / "planner.md").write_text("---\nname: planner\n---\n")
    (agency / "rules" / "build" / "python-cleanup.md").write_text("# cleanup\n")
    (agency / "hooks" / "core" / "safety-check.py").write_text("print('ok')\n")
    (agency / "hooks" / "core" / "safety-patterns.yaml").write_text("patterns: []\n")
    (agency / "hooks-meta.yaml").write_text(
        """\
core/safety-check:
  events:
    PreToolUse:
      matcher: Bash
""",
        encoding="utf-8",
    )
    (claude_src / "settings.json").write_text("{}", encoding="utf-8")

    monkeypatch.setattr(settings, "AGENCY_DIR", agency)
    monkeypatch.setattr(settings, "CLAUDE_SRC", claude_src)
    monkeypatch.setattr(settings, "CLAUDE_DIR", tmp_path / "global-claude")
    monkeypatch.setattr(
        settings,
        "CURRENT_PROFILE_FILE",
        tmp_path / "global-state" / "current-profile",
    )

    selections = setup_core.Selections(
        based_on="build",
        agents={"core": ["core/planner"]},
        rules={"build": ["build/python-cleanup"]},
        hooks=["core/safety-check"],
        mcps=[],
    )

    setup_core.apply(
        tmp_path,
        selections,
        platforms=["claude"],
        claude_dir=install_dir,
        active_name="build",
    )

    managed = load_managed_state(install_dir)

    assert managed["hooks"] == ["safety-check.py"]
    assert (install_dir / "hooks" / "safety-check.py").exists()
    assert not (install_dir / "hooks" / "core" / "safety-check.py").exists()


def test_system_verify_prefers_project_install_dir(tmp_path: Path, monkeypatch: Any) -> None:
    from cli import settings
    from cli.app import main

    project_dir = tmp_path / ".claude"
    project_dir.mkdir()
    (tmp_path / ".rune").mkdir()
    (tmp_path / ".rune" / "current-profile").write_text("build\n")
    (project_dir / settings.MANAGED_STATE_FILE).write_text(
        json.dumps({"agents": [], "rules": [], "hooks": [], "skills": []})
    )
    monkeypatch.setattr(settings, "CURRENT_PROFILE_FILE", tmp_path / "global-state" / "current-profile")

    runner = CliRunner()
    old_cwd = Path.cwd()
    os.chdir(tmp_path)
    try:
        result = runner.invoke(main, ["--source-dir", str(ROOT), "system", "verify"])
    finally:
        os.chdir(old_cwd)

    assert result.exit_code == 0, result.output
    assert f"==> Verifying {project_dir}" in result.output
    assert "Active profile: build [project]" in result.output


def test_reset_supports_project_scope_without_touching_global_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from cli import settings
    from cli.commands.deploy import top_reset

    runner = CliRunner()
    global_dir = tmp_path / "global-claude"
    project_dir = tmp_path / ".claude"
    global_state_file = tmp_path / "global-state" / "current-profile"
    project_state_file = tmp_path / ".rune" / "current-profile"
    local_profile = tmp_path / ".local-profile.yaml"

    for directory in (
        global_dir / "agents",
        project_dir / "agents",
        global_state_file.parent,
        project_state_file.parent,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    (global_dir / settings.MANAGED_STATE_FILE).write_text(
        json.dumps({"agents": ["global-agent.md"], "rules": [], "hooks": [], "skills": []}),
        encoding="utf-8",
    )
    (project_dir / settings.MANAGED_STATE_FILE).write_text(
        json.dumps({"agents": ["project-agent.md"], "rules": [], "hooks": [], "skills": []}),
        encoding="utf-8",
    )
    (global_dir / "agents" / "global-agent.md").write_text("global\n", encoding="utf-8")
    (project_dir / "agents" / "project-agent.md").write_text("project\n", encoding="utf-8")
    global_state_file.write_text("default\n", encoding="utf-8")
    project_state_file.write_text("build\n", encoding="utf-8")
    local_profile.write_text("custom: true\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(settings, "CLAUDE_DIR", global_dir)
    monkeypatch.setattr(settings, "CURRENT_PROFILE_FILE", global_state_file)
    monkeypatch.setattr(settings, "LOCAL_PROFILE_FILE", local_profile)
    monkeypatch.setattr(settings, "PROJECT_DIR", None)

    result = runner.invoke(top_reset, ["--project"], input="delete\n")

    assert result.exit_code == 0, result.output
    assert "Claude Code [project]" in result.output
    assert not (project_dir / settings.MANAGED_STATE_FILE).exists()
    assert not (project_dir / "agents" / "project-agent.md").exists()
    assert not project_state_file.exists()
    assert (global_dir / settings.MANAGED_STATE_FILE).exists()
    assert (global_dir / "agents" / "global-agent.md").exists()
    assert global_state_file.exists()
    assert local_profile.exists()


def test_reset_supports_global_scope_without_touching_project_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from cli import settings
    from cli.commands.deploy import top_reset

    runner = CliRunner()
    global_dir = tmp_path / "global-claude"
    project_dir = tmp_path / ".claude"
    global_state_file = tmp_path / "global-state" / "current-profile"
    project_state_file = tmp_path / ".rune" / "current-profile"

    for directory in (
        global_dir / "agents",
        project_dir / "agents",
        global_state_file.parent,
        project_state_file.parent,
    ):
        directory.mkdir(parents=True, exist_ok=True)

    (global_dir / settings.MANAGED_STATE_FILE).write_text(
        json.dumps({"agents": ["global-agent.md"], "rules": [], "hooks": [], "skills": []}),
        encoding="utf-8",
    )
    (project_dir / settings.MANAGED_STATE_FILE).write_text(
        json.dumps({"agents": ["project-agent.md"], "rules": [], "hooks": [], "skills": []}),
        encoding="utf-8",
    )
    (global_dir / "agents" / "global-agent.md").write_text("global\n", encoding="utf-8")
    (project_dir / "agents" / "project-agent.md").write_text("project\n", encoding="utf-8")
    global_state_file.write_text("default\n", encoding="utf-8")
    project_state_file.write_text("build\n", encoding="utf-8")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(settings, "CLAUDE_DIR", global_dir)
    monkeypatch.setattr(settings, "CURRENT_PROFILE_FILE", global_state_file)
    monkeypatch.setattr(settings, "PROJECT_DIR", None)

    result = runner.invoke(top_reset, ["--global"], input="delete\n")

    assert result.exit_code == 0, result.output
    assert "Claude Code [global]" in result.output
    assert not (global_dir / settings.MANAGED_STATE_FILE).exists()
    assert not (global_dir / "agents" / "global-agent.md").exists()
    assert not global_state_file.exists()
    assert (project_dir / settings.MANAGED_STATE_FILE).exists()
    assert (project_dir / "agents" / "project-agent.md").exists()
    assert project_state_file.exists()


def test_resource_list_marks_categorized_hooks_as_deployed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from cli import settings
    from cli.app import main

    agency = tmp_path / "agency"
    install_dir = tmp_path / ".claude"
    (agency / "hooks" / "core").mkdir(parents=True, exist_ok=True)
    install_dir.mkdir(parents=True, exist_ok=True)

    (agency / "hooks" / "core" / "safety-check.py").write_text(
        '"""Block dangerous commands."""\n',
        encoding="utf-8",
    )
    (install_dir / settings.MANAGED_STATE_FILE).write_text(
        json.dumps({"agents": [], "rules": [], "hooks": ["safety-check.py"], "skills": []}),
        encoding="utf-8",
    )

    monkeypatch.setattr(settings, "AGENCY_DIR", agency)
    monkeypatch.setattr(settings, "CLAUDE_DIR", install_dir)

    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--source-dir", str(ROOT), "--format", "json", "resource", "list"],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    hooks = {item["name"]: item for item in payload["hooks"]}
    assert hooks["core/safety-check"]["deployed"] is True


def test_profiles_wire_build_execution_contract() -> None:
    profiles = (ROOT / "profiles.yaml").read_text(encoding="utf-8")

    assert "default:" in profiles
    assert "build:\n      - build/execution-contract" in profiles


def test_profiles_wire_shared_skill_contract() -> None:
    profiles = (ROOT / "profiles.yaml").read_text(encoding="utf-8")

    assert profiles.count("- core/skill-contract") == 5


def test_hook_registry_and_companions_stay_in_sync() -> None:
    yaml = import_module("cli._common").yaml_instance()
    hooks_meta = yaml.load((ROOT / "src" / "rune-agency" / "hooks-meta.yaml").read_text()) or {}
    hook_names = {
        f"{path.relative_to(HOOKS_ROOT).parts[0]}/{path.stem}"
        for path in HOOKS_ROOT.rglob("*.py")
    }

    assert hook_names == set(hooks_meta.keys())
    assert (HOOKS_ROOT / "core" / "safety-patterns.yaml").exists()
    assert (HOOKS_ROOT / "build" / "auto-lint-rules.yaml").exists()


def test_skill_files_have_clean_frontmatter_and_phase_alignment() -> None:
    phase_pat = re.compile(r"(?m)^phase:\s*(explore|plan|build|validate|general)\s*$")

    for skill_file in sorted(SKILLS_DIR.rglob("SKILL.md")):
        text = skill_file.read_text(encoding="utf-8")
        assert text.startswith("---\n"), skill_file
        assert "\n---\n" in text, skill_file
        fm, body = import_module("cli._common").parse_frontmatter(text)
        assert fm.get("description"), skill_file
        rel = skill_file.relative_to(SKILLS_DIR)
        category = rel.parts[0] if len(rel.parts) > 1 else "core"
        expected_phase = "general" if category == "core" else category
        assert fm.get("phase") == expected_phase, skill_file
        body_no_fences = import_module("cli.logic.validation")._strip_fenced_code_blocks(body)
        assert not phase_pat.search(body_no_fences), skill_file
        if category != "core":
            assert "src/rune-agency/skills/core/skill-contract/SKILL.md" in body_no_fences, skill_file


def test_demo_no_animate_guides_the_user() -> None:
    from cli.app import main

    runner = CliRunner()
    result = runner.invoke(main, ["--source-dir", str(ROOT), "demo", "--no-animate"])

    assert result.exit_code == 0, result.output
    assert "guided simulation" in result.output.lower()
    assert "The Four-Phase Model" in result.output
    assert '"plan a REST API for user management"' in result.output
    assert "Artifact handoff:" in result.output
    assert "Project Progress" in result.output
    assert "Workflow Summary" in result.output
    assert "/km-explore" in result.output
    assert "/write-plan" in result.output
    assert "/rune" in result.output
    assert "/judge-audit" in result.output
    assert "PLAN.md" in result.output
    assert "rune profile use explore" in result.output


def test_auto_lint_resolves_relative_paths_from_project_root(tmp_path: Path) -> None:
    target = tmp_path / "pkg" / "example.py"
    target.parent.mkdir(parents=True)
    target.write_text("print('ok')\n", encoding="utf-8")

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    ruff_log = tmp_path / "ruff.log"
    ruff = bin_dir / "ruff"
    ruff.write_text(
        "#!/bin/sh\n"
        'printf "%s|%s\\n" "$PWD" "$*" >> "$RUFF_LOG"\n',
        encoding="utf-8",
    )
    ruff.chmod(0o755)

    env = dict(os.environ)
    env["CLAUDE_PROJECT_DIR"] = str(tmp_path)
    env["RUFF_LOG"] = str(ruff_log)
    env["PATH"] = f"{bin_dir}:{env.get('PATH', '')}"

    subprocess.run(
        [sys.executable, str(_hook_path("auto-lint"))],
        input=json.dumps({"tool_input": {"file_path": "pkg/example.py"}}),
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )

    lines = ruff_log.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert all(line.startswith(f"{tmp_path}|") for line in lines)
    assert str(target) in "\n".join(lines)


def test_on_stage_complete_uses_current_workflow_language(
    tmp_path: Path,
    write_state,
    default_state: dict[str, Any],
) -> None:
    project_dir = tmp_path
    state = dict(default_state)
    state["workflow"] = "feature-implementation"
    state["ticket"] = "RUNE-123"
    state["next_agent"] = "judge"
    write_state(state)

    output = run_hook("on-stage-complete", project_dir)

    assert "[workflow] Active: feature-implementation | stage: build | wave: 1 | ticket: RUNE-123 | mode: interactive" in output
    assert '[workflow] Suggested next owner: judge for "RUNE-123".' in output
