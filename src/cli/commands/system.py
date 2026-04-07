"""System diagnostic and configuration commands."""

from __future__ import annotations

import click

from .deploy import system_configure, system_verify
from .discovery import system_status
from .scripts import system_site, system_validate


@click.group("system")
def system_group() -> None:
    """System diagnostic and configuration commands."""


system_group.add_command(system_verify)
system_group.add_command(system_validate)
system_group.add_command(system_site)
system_group.add_command(system_configure)
system_group.add_command(system_status)
