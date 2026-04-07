from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path

import click

from ..._common import deploy_short_name


def sync_files(
    src: Path,
    dest: Path,
    names: list[str],
    ext: str,
    executable: bool = False,
    managed_set: set[str] | None = None,
    name_transform: Callable[[str], str] | None = None,
) -> None:
    """Copy files from src to dest."""
    dest.mkdir(parents=True, exist_ok=True)
    transform = name_transform or (lambda name: name)
    expected = {f"{transform(name)}{ext}" for name in names}

    for existing in dest.glob(f"*{ext}"):
        if existing.name not in expected:
            if managed_set is None or existing.name not in managed_set:
                continue
            existing.unlink()
            click.echo(f"  – {existing.stem} (removed)")

    for name in names:
        path = src / f"{name}{ext}"
        if not path.exists():
            matches = list(src.rglob(f"{Path(name).name}{ext}"))
            path = matches[0] if len(matches) == 1 else path
        out_name = transform(name)
        if path.exists():
            output = dest / f"{out_name}{ext}"
            shutil.copy2(path, output)
            if executable:
                output.chmod(output.stat().st_mode | 0o111)
            click.echo(f"  ✓ {name}")
        else:
            click.echo(f"  ✗ {name} (not found)")


def deploy_hook_companions(src: Path, dest: Path, names: list[str]) -> None:
    """Copy companion .yaml files for deployed hooks."""
    dest.mkdir(parents=True, exist_ok=True)
    companions: set[Path] = set()
    for name in names:
        category, stem = name.split("/", 1) if "/" in name else ("", name)
        stem_prefix = stem.split("-")[0]
        search_dir = src / category if category else src
        companions.update(search_dir.glob(f"{stem_prefix}-*.yaml"))
        exact = search_dir / f"{stem}.yaml"
        if exact.exists():
            companions.add(exact)

    for companion in companions:
        shutil.copy2(companion, dest / companion.name)
        click.echo(f"  ✓ {companion.name} (companion)")


def sync_dirs(
    src: Path,
    dest: Path,
    names: list[str],
    managed_set: set[str] | None = None,
    name_transform: Callable[[str], str] | None = None,
) -> None:
    """Copy directories from src to dest."""
    dest.mkdir(parents=True, exist_ok=True)
    transform = name_transform or (lambda name: name)
    expected_names = {transform(name) for name in names}

    for existing in (path for path in dest.iterdir() if path.is_dir()):
        if existing.name not in expected_names:
            if managed_set is None or existing.name not in managed_set:
                continue
            shutil.rmtree(existing)
            click.echo(f"  – {existing.name} (removed)")

    for name in names:
        directory = src / name
        if not directory.is_dir():
            click.echo(f"  ✗ {name} (not found)")
            continue
        deployed_name = transform(name)
        output = dest / deployed_name
        shutil.copytree(directory, output, dirs_exist_ok=True)
        for script in output.rglob("*.sh"):
            script.chmod(script.stat().st_mode | 0o111)
        click.echo(f"  ✓ {name} → /{deployed_name}")


def inject_agents(
    src: Path,
    dest: Path,
    names: list[str],
    _platform: str,
    plat_src: Path | None = None,
    managed_set: set[str] | None = None,
) -> None:
    """Deploy agent .md files."""
    dest.mkdir(parents=True, exist_ok=True)
    expected = {f"{deploy_short_name(name)}.md" for name in names}
    if plat_src and plat_src.is_dir():
        expected |= {path.name for path in plat_src.glob("*.md")}

    for existing in dest.glob("*.md"):
        if existing.name not in expected:
            if managed_set is not None and existing.name not in managed_set:
                continue
            existing.unlink()
            click.echo(f"  – {existing.stem} (removed)")

    for name in names:
        agent_file = src / f"{name}.md"
        if not agent_file.exists():
            click.echo(f"  ✗ {name} (not found)")
            continue
        shutil.copy2(agent_file, dest / f"{deploy_short_name(name)}.md")
        click.echo(f"  ✓ {name}")
