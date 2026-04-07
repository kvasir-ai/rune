from __future__ import annotations

from pathlib import Path

from .. import settings
from .._common import deploy_short_name, flatten_section, load_managed_state, save_managed_state
from .profiles import selections_to_profile_dict, state_file_for_install_dir
from .state import compute_content_hash
from .models import Selections


def apply(
    curdir: Path,
    selections: Selections,
    platforms: list[str],
    claude_dir: Path | None = None,
    active_name: str | None = None,
) -> None:
    """Apply the selections to the specified platforms."""
    from ..commands.deploy import configure_profile

    profile_dict = selections_to_profile_dict(selections)
    src = settings.AGENCY_DIR
    claude_src = settings.CLAUDE_SRC
    install_dir = claude_dir or settings.CLAUDE_DIR

    name_to_write = active_name or selections.active_name or selections.based_on
    if name_to_write:
        state_file = state_file_for_install_dir(install_dir)
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(name_to_write + "\n")

    content_hash = compute_content_hash(curdir, selections)
    for _ in platforms:
        managed_state = load_managed_state(install_dir)
        managed_set = {
            section: set(managed_state.get(section, []))
            for section in ("agents", "rules", "hooks", "skills")
        }
        configure_profile(
            profile_dict,
            "claude",
            curdir,
            src,
            install_dir,
            claude_src,
            managed_set=managed_set,
        )
        deployed_agents = {
            f"{deploy_short_name(name)}.md" for name in flatten_section(selections.agents)
        }
        if (claude_src / "agents").is_dir():
            deployed_agents |= {path.name for path in (claude_src / "agents").glob("*.md")}
        save_managed_state(
            install_dir,
            {
                "agents": sorted(deployed_agents),
                "rules": sorted(
                    f"{deploy_short_name(name)}.md"
                    for name in flatten_section(selections.rules)
                ),
                "hooks": sorted(f"{deploy_short_name(name)}.py" for name in selections.hooks),
                "skills": sorted(deploy_short_name(name) for name in selections.skills),
                "content_hash": content_hash,
            },
        )
