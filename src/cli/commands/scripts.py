"""Script wrapper commands for the rune CLI."""

from __future__ import annotations

from pathlib import Path

import click


@click.command("setup")
@click.pass_context
def top_setup(ctx: click.Context) -> None:
    """Interactive setup wizard."""
    from ..logic.setup_wizard import run_setup_wizard  # noqa: PLC0415
    run_setup_wizard(curdir=ctx.obj.curdir)


@click.command("site")
@click.option(
    "--output",
    "output_dir",
    default=None,
    type=click.Path(path_type=Path),
    help="Output directory for the generated site (default: <source-dir>/site/)",
)
@click.pass_context
def system_site(ctx: click.Context, output_dir: Path | None) -> None:
    """Generate a static documentation site for this rune installation."""
    from ..site import generate  # noqa: PLC0415
    generate(root_dir=ctx.obj.curdir, site_dir=output_dir)


@click.command("validate")
@click.pass_context
def system_validate(ctx: click.Context) -> None:
    """Validate YAML files against JSON schemas."""
    click.echo("==> Validating YAML against schemas")
    from ..logic.validation import validate_schemas  # noqa: PLC0415
    if not validate_schemas(root_dir=ctx.obj.curdir):
        raise click.ClickException("Validation failed.")


@click.command("budget")
def profile_budget() -> None:
    """Show token footprint for the active profile."""
    click.echo("Context budget estimation moved to site generator.")
    click.echo("Use 'rune profile show <name>' to see deployed rules.")
