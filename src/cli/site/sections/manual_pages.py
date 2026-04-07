"""Manual page sections rendered through a small Jinja template layer."""
from __future__ import annotations

import re
from pathlib import Path

from ruamel.yaml import YAML

from ..components import esc
from ..render import render_template


def _yaml() -> YAML:
    parser = YAML()
    parser.default_flow_style = False
    parser.allow_unicode = True
    parser.allow_duplicate_keys = True
    return parser


def _load_yaml(path: Path) -> dict:
    return _yaml().load(path.read_text(encoding="utf-8")) or {}


def _load_profile_blocks(path: Path) -> list[tuple[str, str, str]]:
    text = path.read_text(encoding="utf-8")
    entries: list[tuple[str, str, str]] = []
    current_name: str | None = None
    current_lines: list[str] = []
    current_description = ""

    def flush() -> None:
        nonlocal current_name, current_lines, current_description
        if current_name and current_name != "global_rules":
            block = "\n".join(current_lines).rstrip()
            entries.append((current_name, current_description, block))
        current_name = None
        current_lines = []
        current_description = ""

    for line in text.splitlines():
        top_level = re.match(r"^([A-Za-z0-9_-]+):\s*$", line)
        if top_level:
            flush()
            current_name = top_level.group(1)
            current_lines = [line]
            continue
        if current_name is None:
            continue
        current_lines.append(line)
        description_match = re.match(r"^  description:\s*['\"]?(.*?)['\"]?\s*$", line)
        if description_match:
            current_description = description_match.group(1)

    flush()
    return entries


def _code(text: str) -> str:
    return f'<code class="copyable">{esc(text)}</code>'


def _nav_code(section: str, text: str) -> str:
    return f'<button data-section="{esc(section)}">{_code(text)}</button>'


def _link(url: str) -> str:
    return f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(url)}</a>'


def _command_groups() -> list[dict[str, object]]:
    return [
        {
            "section_id": "rune-cli-top",
            "label": "Top-Level",
            "page_title": "Top-Level Commands",
            "command_name": "rune",
            "synopsis": "rune <command>",
            "description": "Bootstrap, preview, and reset the rune environment.",
            "rows": [
                (_code("rune setup"), "Interactive setup wizard."),
                (_code("rune demo"), "Show the Four Phase Model workflow demo."),
                (_code("rune reset [--global|--project]"), "Remove managed resources from the selected install scope."),
            ],
        },
        {
            "section_id": "rune-cli-profile",
            "label": "Profiles",
            "page_title": "Profile Commands",
            "command_name": "rune profile",
            "synopsis": "rune profile <subcommand> [args]",
            "description": "Manage environments and knowledge profiles.",
            "rows": [
                (_code("rune profile use NAME"), "Apply a profile and deploy its resources."),
                (_code("rune profile list"), "List all available profiles."),
                (_code("rune profile current"), "Print the name of the active profile."),
                (_code("rune profile reapply"), "Re-apply the current active profile."),
                (_code("rune profile budget"), "Show the token footprint for the active profile."),
            ],
        },
        {
            "section_id": "rune-cli-resource",
            "label": "Resources",
            "page_title": "Resource Commands",
            "command_name": "rune resource",
            "synopsis": "rune resource <subcommand>",
            "description": "Inspect available agents, rules, and skills.",
            "rows": [
                (_code("rune resource list"), "List all available resources."),
                (_code("rune resource skills"), "List available skills with descriptions."),
                (_code("rune resource tools"), "List available system tools."),
            ],
        },
        {
            "section_id": "rune-cli-system",
            "label": "System",
            "page_title": "System Commands",
            "command_name": "rune system",
            "synopsis": "rune system <subcommand>",
            "description": "Diagnostic and internal configuration utilities.",
            "rows": [
                (_code("rune system verify"), "Verify installed resources."),
                (_code("rune system validate"), "Validate YAML files against JSON schemas."),
                (_code("rune system site"), "Generate this documentation site."),
            ],
        },
        {
            "section_id": "rune-cli-mcp",
            "label": "MCP",
            "page_title": "MCP Commands",
            "command_name": "rune mcp",
            "synopsis": "rune mcp <subcommand> [name]",
            "description": "Manage Model Context Protocol (MCP) servers.",
            "rows": [
                (_code("rune mcp list"), "List all available MCPs."),
                (_code("rune mcp status"), "Show MCP status for the active or selected profile."),
                (_code("rune mcp enable NAME"), "Enable an MCP in the current profile."),
                (_code("rune mcp disable NAME"), "Disable an MCP."),
            ],
        },
    ]


def build_manual_pages(root: Path) -> str:
    profiles = _load_profile_blocks(root / "profiles.yaml")
    registry = _load_yaml(root / "tools" / "registry.yaml")

    available_profile_rows = [
        (_code(name), esc(description)) for name, description, _ in profiles
    ]
    example_profile_block = next(
        (block for name, _, block in profiles if name == "build"),
        profiles[0][2] if profiles else "",
    )

    available_tool_rows = []
    for name, data in registry.items():
        binary = str(data.get("binary", ""))
        description = esc(str(data.get("description", "")))
        check = esc(str(data.get("check", "")))
        url = str(data.get("url", ""))
        available_tool_rows.append(
            (
                _code(str(name)),
                _code(binary),
                description,
                check if check else "&mdash;",
                _link(url),
            )
        )

    command_summary_rows = [
        (_nav_code("rune-cli-top", "setup | demo | reset"), "Bootstrap, preview, and reset the rune environment."),
        (_nav_code("rune-cli-profile", "profile ..."), "Select, inspect, and reapply profiles."),
        (_nav_code("rune-cli-resource", "resource ..."), "Inspect deployed agents, rules, skills, and tools."),
        (_nav_code("rune-cli-system", "system ..."), "Verify deployment state, validate configuration, and rebuild docs."),
        (_nav_code("rune-cli-mcp", "mcp ..."), "Inspect and manage MCP integrations by profile."),
    ]

    cheatsheet_cards = [
        {
            "section_id": "rune-cli-top",
            "emoji": "&#x1F527;",
            "title": "Setup & Reset",
            "command": _code("rune setup"),
            "purpose": "Bootstrap Rune the first time, preview the workflow with the demo, or wipe the selected global or project-local install with reset.",
        },
        {
            "section_id": "rune-cli-profile",
            "emoji": "&#x1F504;",
            "title": "Profiles",
            "command": _code("rune profile use NAME"),
            "purpose": "Apply, inspect, and reapply the profile that matches the work in front of you.",
        },
        {
            "section_id": "rune-cli-resource",
            "emoji": "&#x1F4E6;",
            "title": "Resources",
            "command": _code("rune resource list"),
            "purpose": "Inspect the active agents, rules, skills, and tools after setup or profile changes.",
        },
        {
            "section_id": "rune-cli-system",
            "emoji": "&#x2699;&#xFE0F;",
            "title": "System Checks",
            "command": _code("rune system verify"),
            "purpose": "Confirm deployed state, validate configuration, and regenerate the docs site when needed.",
        },
        {
            "section_id": "rune-cli-mcp",
            "emoji": "&#x1F50C;",
            "title": "MCP",
            "command": _code("rune mcp status"),
            "purpose": "Inspect which MCP integrations are enabled and then enable or disable them by profile.",
        },
    ]

    man_example_rows = [
        (_code("rune setup"), "Run the interactive bootstrap flow."),
        (_code("rune profile use build --project"), "Apply a project-local build profile."),
        (_code("rune reset --project"), "Remove managed resources from the current repo only."),
        (_code("rune resource list"), "Inspect the active resource surface."),
        (_code("rune system verify"), "Check the deployed state after setup or profile changes."),
    ]

    return render_template(
        "manual_pages.html",
        cheatsheet_cards=cheatsheet_cards,
        command_summary_rows=command_summary_rows,
        man_options_rows=[
            (_code("--format [text|json]"), "Output format (default: text)"),
            (_code("--curdir PATH"), "Repository root directory"),
            (_code("-h, --help"), "Show the help message and exit."),
        ],
        man_example_rows=man_example_rows,
        command_groups=_command_groups(),
        exit_status_rows=[
            (_code("0"), "Success."),
            (_code("1"), "Error or validation failure."),
        ],
        environment_rows=[
            (_code("RUNE_SOURCE_DIR"), "rune source repository root."),
            (_code("RUNE_PROJECT_DIR"), "project-local install target."),
        ],
        profile_file_rows=[
            (_code("profiles.yaml"), "Define shared profiles and global rules."),
            (_code(".local-profile.yaml"), "Keep personal profiles out of the shared repo."),
            (_code("schemas/profiles.schema.json"), "Validate profile structure."),
        ],
        profile_field_rows=[
            (_code("description"), "Describe the job the profile supports."),
            (_code("agents"), "Group the agents the profile loads."),
            (_code("rules"), "Load rule files by phase or category."),
            (_code("skills"), "Expose task-specific workflows."),
            (_code("hooks"), "Enable runtime checks and guardrails."),
            (_code("mcps"), "Enable optional MCP integrations."),
            (_code("global_rules"), "Apply shared rules to every profile."),
        ],
        available_profile_rows=available_profile_rows,
        example_profile_block=example_profile_block,
        profile_create_steps=[
            f'Choose {_code("profiles.yaml")} for a shared profile or {_code(".local-profile.yaml")} for a personal profile.',
            "Copy an existing top-level profile block.",
            f'Rename the block and update {_code("description")}.',
            (
                f'Keep only the {_code("agents")}, {_code("rules")}, {_code("skills")}, '
                f'{_code("hooks")}, and {_code("mcps")} the work needs.'
            ),
            f'Run {_code("rune system validate")}.',
            f'Apply it with {_code("rune profile use NAME")}.',
            f'Check the result with {_code("rune profile current")} and {_code("rune profile budget")}.',
        ],
        tools_file_rows=[
            (_code("tools/registry.yaml"), "Register each tool and its metadata."),
            (_code("tools/<name>/install-<name>.sh"), "Install script for one tool."),
            (_code("tools/<name>/uninstall-<name>.sh"), "Uninstall script for one tool."),
        ],
        registry_field_rows=[
            (_code("binary"), "Command Rune checks after install."),
            (_code("description"), "Short label shown in docs and setup flows."),
            (_code("url"), "Upstream project URL."),
            (_code("check"), "Optional custom verification command when a binary check is not enough."),
        ],
        available_tool_rows=available_tool_rows,
        tool_add_steps=[
            f'Add a new entry to {_code("tools/registry.yaml")}.',
            f'Create {_code("tools/<name>/install-<name>.sh")} and {_code("tools/<name>/uninstall-<name>.sh")}.',
            f'Use {_code("check")} only when the default binary check is not enough.',
            (
                f'Install the tool or make sure it is already on your {_code("PATH")}, '
                f'then run {_code("rune system verify")}.'
            ),
        ],
    )
