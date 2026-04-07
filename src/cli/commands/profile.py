"""Profile management commands."""

from __future__ import annotations

import click

from .._common import (
    active_profile,
    pass_toolkit,
    ToolkitContext,
)
from .deploy import profile_use, profile_delete, profile_reapply, profile_toggle
from .discovery import profile_list, profile_show
from .scripts import profile_budget


@click.group("profile")
def profile_group() -> None:
    """Profile management commands."""


@profile_group.command("current")
@pass_toolkit
def profile_current(ctx: ToolkitContext) -> None:
    """Print the active profile name."""
    click.echo(active_profile(ctx.curdir))


profile_group.add_command(profile_use)
profile_group.add_command(profile_delete)
profile_group.add_command(profile_reapply)
profile_group.add_command(profile_toggle)
profile_group.add_command(profile_list)
profile_group.add_command(profile_show)
profile_group.add_command(profile_budget)
