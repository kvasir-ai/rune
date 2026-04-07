from __future__ import annotations

import dataclasses
import io
import shutil
from pathlib import Path

from ruamel.yaml import YAML

__all__ = [
    'ToolkitError',
    'yaml_instance',
    'load_profiles_yaml',
    'active_profile',
    'active_profile_state_file',
    'flatten_section',
    'parse_frontmatter',
    'detect_platforms',
    'save_profiles_yaml',
    'resolve_profile',
    'load_managed_state',
    'save_managed_state',
    'deploy_short_name',
    'pass_toolkit',
    'get_profile',
    'ToolkitContext',
]

pass_toolkit: object


class ToolkitError(Exception):
    """Expected errors (missing files, invalid config); catch at CLI boundary."""


@dataclasses.dataclass
class ToolkitContext:
    format: str  # "text" or "json"
    curdir: Path  # repo root


def __getattr__(name: str):
    if name == 'pass_toolkit':
        import click

        val = click.make_pass_decorator(ToolkitContext, ensure=True)
        globals()['pass_toolkit'] = val
        return val
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')


def get_profile(profiles: dict, name: str) -> dict:
    """Return a profile by name or raise ToolkitError."""
    if name == 'global_rules':
        raise ToolkitError("'global_rules' is not a profile")
    if name not in profiles:
        raise ToolkitError(f"Profile '{name}' not found")
    return profiles[name]


_yaml: YAML | None = None


def yaml_instance() -> YAML:
    """Return the shared ruamel.yaml instance."""
    global _yaml
    if _yaml is None:
        _yaml = YAML()
        _yaml.default_flow_style = False
        _yaml.allow_unicode = True
    return _yaml


def load_profiles_yaml(_curdir: Path) -> dict:
    """Load profiles.yaml from settings."""
    from . import settings

    f = settings.PROFILES_FILE
    if not f.exists():
        raise ToolkitError(f'profiles.yaml not found at {f}')
    return yaml_instance().load(f.read_text()) or {}


def save_profiles_yaml(path: Path, data: dict) -> None:
    """Write profile data to the given path."""
    buf = io.StringIO()
    yaml_instance().dump(data, buf)
    path.write_text(buf.getvalue())


def active_profile_state_file() -> Path | None:
    """Return the active profile state file, preferring project scope."""
    from . import settings

    project_file = Path.cwd() / '.rune' / 'current-profile'
    if project_file.exists():
        return project_file
    global_file = settings.CURRENT_PROFILE_FILE
    if global_file.exists():
        return global_file
    return None


def active_profile(_curdir: Path) -> str:
    """Determine the active profile name from local or global settings."""
    state_file = active_profile_state_file()
    if state_file is not None:
        return state_file.read_text().strip()
    return 'default'


def resolve_profile(profile: str | None, curdir: Path) -> str:
    """Return profile if given, otherwise fall back to active_profile."""
    return profile if profile else active_profile(curdir)


def flatten_section(items: list[str] | dict[str, list[str]]) -> list[str]:
    """Normalize a profile section to a flat list of names."""
    if isinstance(items, list):
        return items
    if isinstance(items, dict):
        result: list[str] = []
        for names in items.values():
            if names:
                result.extend(names)
        return result
    return []


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter block from a markdown string."""
    if not text.startswith('---'):
        return {}, text
    try:
        end = text.index('\n---', 3)
    except ValueError:
        return {}, text
    fm = yaml_instance().load(text[3:end]) or {}
    body = text[end + 4 :].lstrip('\n')
    return dict(fm), body


def detect_platforms() -> list[str]:
    """Detect available AI coding platforms on the system."""
    from . import settings

    if shutil.which('claude') or settings.CLAUDE_DIR.exists():
        return ['claude']
    return []


def load_managed_state(platform_dir: Path) -> dict:
    """Load deployment state from the platform directory."""
    import json as _json

    from . import settings

    f = platform_dir / settings.MANAGED_STATE_FILE
    if f.exists():
        try:
            return _json.loads(f.read_text())
        except (_json.JSONDecodeError, AttributeError):
            pass
    return {}


def save_managed_state(platform_dir: Path, state: dict) -> None:
    """Save deployment state to the platform directory."""
    import json as _json

    from . import settings

    platform_dir.mkdir(parents=True, exist_ok=True)
    f = platform_dir / settings.MANAGED_STATE_FILE
    f.write_text(_json.dumps(state, indent=2) + '\n')


def deploy_short_name(name: str) -> str:
    """Extract the short name from a 'category/name' resource string."""
    return name.split('/', 1)[1] if '/' in name else name


def _json_out(data: dict | list) -> None:
    """Print JSON to stdout."""
    import json as _json

    import click

    click.echo(_json.dumps(data, indent=2))
