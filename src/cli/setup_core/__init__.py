from __future__ import annotations

from .apply import apply
from .discovery import discover, discover_tools
from .models import AvailableContent, CurrentState, Selections, Tool
from .profiles import (
    _load_local_profile_yaml,
    _load_profiles_yaml,
    _regroup_by_filesystem,
    compute_profile_hash,
    delete_local_profile,
    export_to_local_profile_yaml,
    export_to_profiles_yaml,
    list_profiles,
    load_base_profile,
    load_profile,
    selections_to_profile_dict,
    state_file_for_install_dir,
    variant_name,
)
from .state import (
    check_base_drift,
    check_content_drift,
    compute_content_hash,
    detect_current_state,
    diff_from_base,
    list_unmanaged,
)

__all__ = [
    "AvailableContent",
    "Tool",
    "Selections",
    "CurrentState",
    "variant_name",
    "list_profiles",
    "load_profile",
    "load_base_profile",
    "delete_local_profile",
    "discover",
    "discover_tools",
    "detect_current_state",
    "compute_profile_hash",
    "compute_content_hash",
    "state_file_for_install_dir",
    "check_base_drift",
    "check_content_drift",
    "diff_from_base",
    "selections_to_profile_dict",
    "export_to_profiles_yaml",
    "export_to_local_profile_yaml",
    "list_unmanaged",
    "apply",
    "_load_profiles_yaml",
    "_load_local_profile_yaml",
    "_flatten_section",
    "_regroup_by_filesystem",
]

from .._common import flatten_section as _flatten_section
