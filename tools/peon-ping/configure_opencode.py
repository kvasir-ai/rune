#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6.0"]
# ///
"""
Peon-Ping Configuration for OpenCode

Configures peon-ping for model-based random pack rotation on OpenCode.
Installs packs and writes configuration. Model-switching hooks are
pending OpenCode's hook API investigation.

Profiles are defined in tools/peon-ping/profiles.yaml.
"""

import json
import subprocess
import sys
import os
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Run: uv add pyyaml")
    sys.exit(1)


PROFILES_YAML = Path(__file__).parent / "profiles.yaml"
DEFAULT_PROFILES = ["warcraft", "redalert"]


def _load_profiles() -> dict[str, dict[str, list[str]]]:
    """Load profiles from YAML file."""
    if not PROFILES_YAML.is_file():
        print(f"ERROR: {PROFILES_YAML} not found")
        sys.exit(1)
    with open(PROFILES_YAML) as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        print(f"ERROR: {PROFILES_YAML} must be a YAML mapping")
        sys.exit(1)
    return data


def _resolve_profiles() -> list[str]:
    """Resolve which profiles to use from PEON_PROFILES env var."""
    profiles = _load_profiles()
    raw = os.environ.get("PEON_PROFILES", "").strip()
    if not raw:
        return list(DEFAULT_PROFILES)
    names = [p.strip() for p in raw.split(",") if p.strip()]
    invalid = [n for n in names if n not in profiles]
    if invalid:
        print(f"ERROR: Unknown profile(s): {', '.join(invalid)}")
        print(f"Available: {', '.join(sorted(profiles))}")
        sys.exit(1)
    return names


def _build_tier_lists(profile_names: list[str]) -> tuple[list[str], list[str], list[str]]:
    """Merge selected profiles into haiku/sonnet/opus pack lists."""
    profiles = _load_profiles()
    haiku: list[str] = []
    sonnet: list[str] = []
    opus: list[str] = []
    for name in profile_names:
        profile = profiles[name]
        haiku.extend(p for p in profile.get("haiku", []) if p not in haiku)
        sonnet.extend(p for p in profile.get("sonnet", []) if p not in sonnet)
        opus.extend(p for p in profile.get("opus", []) if p not in opus)
    return haiku, sonnet, opus


_selected = _resolve_profiles()
HAIKU_PACKS, SONNET_PACKS, OPUS_PACKS = _build_tier_lists(_selected)
ALL_PACKS = HAIKU_PACKS + SONNET_PACKS + OPUS_PACKS

# Paths (OpenCode uses ~/.openpeon/ instead of Claude Code's .claude/hooks/peon-ping/)
PACKS_DIR = Path.home() / ".openpeon" / "packs"
PEON_CONFIG_DIR = (
    Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    / "opencode"
    / "peon-ping"
)
CONFIG = PEON_CONFIG_DIR / "config.json"

# Try to find Claude Code's peon.sh for pack installation
PEON_SH = (
    Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude"))
    / "hooks"
    / "peon-ping"
    / "peon.sh"
)


def preflight_check() -> bool:
    """Check if peon-ping for OpenCode is installed."""
    if not PEON_CONFIG_DIR.is_dir():
        print(f"ERROR: peon-ping for OpenCode not found at {PEON_CONFIG_DIR}")
        print("Install it first: bash adapters/opencode.sh")
        return False
    return True


def install_missing_packs():
    """Install all required packs if not already present."""
    print("--- Step 1: Installing missing packs ---")

    PACKS_DIR.mkdir(parents=True, exist_ok=True)

    if PEON_SH.is_file():
        # Use Claude Code's peon.sh for pack downloads
        for pack in ALL_PACKS:
            pack_path = PACKS_DIR / pack
            if pack_path.is_dir():
                print(f"  [skip]    {pack}")
            else:
                print(f"  [install] {pack}")
                try:
                    env = os.environ.copy()
                    env["PEON_PACKS_DIR"] = str(PACKS_DIR)
                    result = subprocess.run(
                        [str(PEON_SH), "packs", "install", pack],
                        capture_output=True,
                        text=True,
                        timeout=30,
                        env=env,
                    )
                    for line in result.stdout.split("\n"):
                        if any(x in line for x in ["[", "Warning", "Error"]):
                            print(f"    {line}")
                except subprocess.TimeoutExpired:
                    print(f"    [timeout] {pack}")
    else:
        print(f"  WARNING: peon.sh not found at {PEON_SH}")
        print(f"  Cannot auto-install packs. Install them manually to {PACKS_DIR}")
        print("  Or install Claude Code's peon-ping first, then re-run this script.")

    print()


def patch_config_json():
    """Set pack_rotation_mode and model_packs in config.json."""
    print("--- Step 2: Patching config.json ---")

    try:
        with open(CONFIG) as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}

    config["pack_rotation_mode"] = "session_override"
    config["model_packs"] = {
        "haiku": HAIKU_PACKS,
        "sonnet": SONNET_PACKS,
        "opus": OPUS_PACKS,
    }

    with open(CONFIG, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    print("  pack_rotation_mode = session_override")
    print("  model_packs = configured (haiku/sonnet/opus)")
    print()


def print_model_switching_info():
    """Print information about pending model-switching hooks."""
    print("--- Step 3: Model-switching hooks ---")
    print("  TODO: OpenCode uses TypeScript plugins, not shell hooks.")
    print("  The model_packs config has been written to config.json.")
    print("  A TypeScript plugin extension is needed to read the active model")
    print("  and pick a random pack from the matching tier.")
    print()
    print("  When OpenCode's hook API is known, this script will be updated to:")
    print("    1. Create/extend the peon-ping.ts plugin with model detection")
    print("    2. Auto-switch packs on model change (like Claude Code's hooks)")
    print()


def print_summary():
    """Print configuration summary."""
    print("=== Done ===")
    print()
    print(f"  haiku  ({len(HAIKU_PACKS)} packs): {' '.join(HAIKU_PACKS)}")
    print(f"  sonnet ({len(SONNET_PACKS)} packs): {' '.join(SONNET_PACKS)}")
    print(f"  opus   ({len(OPUS_PACKS)} packs):  {' '.join(OPUS_PACKS)}")
    print()
    print("  Packs installed. Model-switching hooks pending.")
    print("  Restart OpenCode to pick up config changes.")


def main():
    print("=== Peon-Ping Model Pack Configuration (OpenCode) ===")
    print(f"Config:  {CONFIG}")
    print(f"Packs:   {PACKS_DIR}")
    print()

    if not preflight_check():
        sys.exit(1)

    install_missing_packs()
    patch_config_json()
    print_model_switching_info()
    print_summary()


if __name__ == "__main__":
    main()
