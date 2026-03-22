#!/usr/bin/env python3
"""
Peon-Ping Configuration for OpenCode

Configures peon-ping for model-based random pack rotation on OpenCode.
Installs packs and writes configuration. Model-switching hooks are
pending OpenCode's hook API investigation.
"""

import json
import subprocess
import sys
import os
from pathlib import Path


# Pack assignments by model tier
HAIKU_PACKS = [
    "peon",
    "peasant",
    "warcraft-peon",
    "wc2_peasant",
    "ra2_soviet_engineer",
    "murloc",
]
SONNET_PACKS = [
    "wc3_grunt",
    "wc3_knight",
    "ra_soviet",
    "ra2_kirov",
    "ra2_peon",
    "wow-tauren",
]
OPUS_PACKS = [
    "wc3_corrupted_arthas",
    "wc3_brewmaster",
    "wc3_farseer",
    "wc3_jaina",
    "ra2_eva_commander",
    "ra2_yuri",
    "red-alert-1-eva",
]
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
