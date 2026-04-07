"""Command modules for the rune CLI."""

from __future__ import annotations

import click


def register_commands(cli: click.Group) -> None:
    from .demo import top_demo
    from .deploy import top_reset
    from .mcp import mcp_group
    from .profile import profile_group
    from .resource import resource_group
    from .scripts import top_setup
    from .system import system_group

    cli.add_command(profile_group)
    cli.add_command(resource_group)
    cli.add_command(system_group)
    cli.add_command(mcp_group)
    cli.add_command(top_reset)
    cli.add_command(top_demo)
    cli.add_command(top_setup)
