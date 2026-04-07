from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from ._common import ToolkitContext, ToolkitError


class ToolkitGroup(click.Group):
    """Click Group that catches ToolkitError and exits cleanly."""

    def invoke(self, ctx: click.Context) -> object:
        try:
            return super().invoke(ctx)
        except (ToolkitError, ValueError, FileNotFoundError) as e:
            fmt = ctx.obj.format if ctx.obj else 'text'
            if fmt == 'json':
                click.echo(json.dumps({'error': str(e)}))
            else:
                click.echo(str(e), err=True)
            sys.exit(1)
        except (SystemExit, click.exceptions.Exit, click.exceptions.Abort):
            raise
        except Exception as e:
            fmt = ctx.obj.format if ctx.obj else 'text'
            if fmt == 'json':
                click.echo(json.dumps({'error': str(e)}))
            else:
                click.echo(str(e), err=True)
            sys.exit(1)


@click.group(
    cls=ToolkitGroup,
    epilog="""\b
EXAMPLES:
  rune setup                 Interactively initialize your environment.
  rune profile use explore   Apply the explore profile.
  rune demo                  Run a showcase of the Four-Phase Model.
  rune system status         Check current deployment state.
\b
ENVIRONMENT:
  RUNE_SOURCE_DIR    rune source repository root.
  RUNE_PROJECT_DIR   project-local install target; if set, implies --project automatically.
""",
)
@click.option(
    '--format',
    'fmt',
    type=click.Choice(['text', 'json']),
    default='text',
    help='Output format (default: text)',
)
@click.option(
    '--source-dir',
    'curdir',
    default=None,
    type=click.Path(path_type=Path),
    help='rune source repository root (overrides RUNE_SOURCE_DIR)',
)
@click.pass_context
def main(ctx: click.Context, fmt: str, curdir: Path | None) -> None:
    """Rune Agency (rune) - A command-line toolkit for AI agent orchestration."""
    from . import settings

    if curdir:
        settings.REPO_ROOT = curdir
        settings.AGENCY_DIR = curdir / 'src' / 'rune-agency'
        settings.PROFILES_FILE = curdir / 'profiles.yaml'
        settings.LOCAL_PROFILE_FILE = curdir / '.local-profile.yaml'
        settings.CLAUDE_SRC = curdir / 'platforms' / 'claude'
    ctx.obj = ToolkitContext(
        format=fmt,
        curdir=settings.REPO_ROOT,
    )


from .commands import register_commands  # noqa: E402

register_commands(main)


if __name__ == "__main__":
    main()
