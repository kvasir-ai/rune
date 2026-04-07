"""Resource management commands."""

from __future__ import annotations

import click

from .discovery import resource_list
from .metadata import resource_skills, resource_tools


@click.group("resource")
def resource_group() -> None:
    """Resource management commands."""


resource_group.add_command(resource_list)
resource_group.add_command(resource_tools)
resource_group.add_command(resource_skills)
