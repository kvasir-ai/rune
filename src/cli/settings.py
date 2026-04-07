"""Global settings and environment configuration for the rune CLI."""

import os
from pathlib import Path

# Platform Paths
CLAUDE_DIR = Path.home() / ".claude"  # global install target (always ~/.claude/)
_project_dir_env = os.getenv("RUNE_PROJECT_DIR")
PROJECT_DIR: Path | None = Path(_project_dir_env) if _project_dir_env else None

# Repository and Agency Detection
def _detect_paths():
    # 1. Environment variable priority
    if env_source := os.getenv("RUNE_SOURCE_DIR"):
        root = Path(env_source)
        agency = root / "src" / "rune-agency"
        if not agency.exists():
            agency = root / "rune-agency"
        return root, agency

    # 2. Try to detect relative to this file
    # Source tree: src/cli/settings.py -> parent.parent.parent
    # Installed: cli/settings.py -> parent.parent
    file_path = Path(__file__).resolve()
    
    # Check for source tree
    pot_root = file_path.parent.parent.parent
    if (pot_root / "src" / "rune-agency").exists():
        return pot_root, pot_root / "src" / "rune-agency"
        
    # Check for installed structure
    pot_root = file_path.parent.parent
    if (pot_root / "rune-agency").exists():
        return pot_root, pot_root / "rune-agency"

    # 3. Default to PROJECT_DIR or CWD
    root = PROJECT_DIR if PROJECT_DIR else Path.cwd()
    agency = root / "src" / "rune-agency"
    if not agency.exists():
        agency = root / "rune-agency"
    return root, agency

REPO_ROOT, AGENCY_DIR = _detect_paths()

# Configuration Files
PROFILES_FILE = REPO_ROOT / "profiles.yaml"
if not PROFILES_FILE.exists() and (REPO_ROOT / "src" / "rune-agency" / "profiles.yaml").exists():
    PROFILES_FILE = REPO_ROOT / "src" / "rune-agency" / "profiles.yaml"

LOCAL_PROFILE_FILE = REPO_ROOT / ".local-profile.yaml"
RUNE_STATE_DIR = Path.home() / ".rune"
CURRENT_PROFILE_FILE = RUNE_STATE_DIR / "current-profile"  # global state

# Platform Source (used for deployment)
CLAUDE_SRC = REPO_ROOT / "platforms" / "claude"
if not CLAUDE_SRC.exists() and (REPO_ROOT / "src" / "rune-agency" / "platforms" / "claude").exists():
    CLAUDE_SRC = REPO_ROOT / "src" / "rune-agency" / "platforms" / "claude"

# State Tracking
MANAGED_STATE_FILE = ".rune-managed.json"

# Constants
DEFAULT_TIMEOUT = 30
HASH_LEN = 8
MAX_DESCRIPTION_LEN = 70

# Category prefixes for grouping skills
SKILL_CATEGORY_PREFIXES = {"core", "explore", "plan", "build", "validate"}

# Resource extensions
EXT_MAP = {"agents": ".md", "rules": ".md", "hooks": ".py"}
