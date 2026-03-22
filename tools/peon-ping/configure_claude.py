#!/usr/bin/env python3
"""
Peon-Ping Configuration for Claude Code

Configures peon-ping for model-based random pack rotation.
Sets up SessionStart/UserPromptSubmit hooks to automatically
pick and switch packs based on the active Claude model tier (haiku/sonnet/opus).

Profiles control which sound packs are included. Select one or more:
    make configure-peon PEON_PROFILES=warcraft,redalert

Available profiles:
    warcraft       Warcraft series (EN)
    warcraft-ru    Warcraft series (RU)
    redalert       Red Alert / C&C series (EN)
    starcraft      StarCraft series (EN)
    shooter        FPS mix (CS, TF2, Halo, Duke Nukem, Helldivers 2)
    sci-fi         Sci-fi AI voices (GLaDOS, Cortana, HAL 9000)
"""

import json
import subprocess
import sys
import os
from pathlib import Path


def _is_wsl() -> bool:
    """Detect if running under WSL."""
    try:
        return "microsoft" in Path("/proc/version").read_text().lower()
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Profile definitions — each profile maps packs to model tiers.
#
#   haiku:  workers, grunts, low-tier units
#   sonnet: mid-tier units, soldiers, vehicles
#   opus:   heroes, commanders, bosses
# ---------------------------------------------------------------------------

PROFILES: dict[str, dict[str, list[str]]] = {
    "warcraft": {
        "haiku": [
            "peon",
            "peasant",
            "warcraft-peon",
            "wc2_peasant",
            "murloc",
        ],
        "sonnet": [
            "wc3_grunt",
            "wc3_knight",
            "wc3_brewmaster",
            "wc3_farseer",
            "wow-tauren",
        ],
        "opus": [
            "wc3_corrupted_arthas",
            "wc3_jaina",
        ],
    },
    "warcraft-ru": {
        "haiku": [
            "peon_ru",
            "peasant_ru",
            "wc2_peon_ru",
        ],
        "sonnet": [
            "acolyte_ru",
            "high_elf_builder_ru",
        ],
        "opus": [
            "arthas_ru",
            "brewmaster_ru",
        ],
    },
    "redalert": {
        "haiku": [
            "ra2_soviet_engineer",
        ],
        "sonnet": [
            "ra_soviet",
            "ra2_kirov",
            "ra2_peon",
        ],
        "opus": [
            "ra2_eva_commander",
            "ra2_yuri",
            "red-alert-1-eva",
        ],
    },
    "starcraft": {
        "haiku": [
            "sc_scv",
            "sc_marine",
            "sc_firebat",
            "sc_medic",
        ],
        "sonnet": [
            "sc_ghost",
            "sc_goliath",
            "sc_dropship",
            "sc_tank",
            "sc_battlecruiser",
            "protoss",
        ],
        "opus": [
            "sc_kerrigan",
            "sc_raynor",
            "sc2_abathur",
            "sc2_alarak",
            "sc2_carrier",
            "sc2_stalker",
            "sc2_stetmann",
        ],
    },
    "shooter": {
        "haiku": [
            "counterstrike",
            "worms-armageddon",
        ],
        "sonnet": [
            "tf2_engineer",
            "tf2_heavy",
            "tf2_demoman",
            "tf2_pyro",
            "tf2_sniper",
            "tf2_spy",
        ],
        "opus": [
            "duke_nukem",
            "halo3_announcer",
            "hd2_helldiver",
        ],
    },
    "sci-fi": {
        "haiku": [
            "cortana",
        ],
        "sonnet": [
            "hal_2001",
        ],
        "opus": [
            "glados",
        ],
    },
}

DEFAULT_PROFILES = ["warcraft", "redalert"]

# Paths
PEON_DIR = (
    Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude"))
    / "hooks"
    / "peon-ping"
)
PEON_SH = PEON_DIR / "peon.sh"
CONFIG = PEON_DIR / "config.json"
SCRIPTS_DIR = PEON_DIR / "scripts"
SETTINGS_JSON = (
    Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")) / "settings.json"
)


def resolve_profiles() -> list[str]:
    """Resolve which profiles to use from PEON_PROFILES env var."""
    raw = os.environ.get("PEON_PROFILES", "").strip()
    if not raw:
        return list(DEFAULT_PROFILES)
    names = [p.strip() for p in raw.split(",") if p.strip()]
    invalid = [n for n in names if n not in PROFILES]
    if invalid:
        print(f"ERROR: Unknown profile(s): {', '.join(invalid)}")
        print(f"Available: {', '.join(sorted(PROFILES))}")
        sys.exit(1)
    return names


def build_tier_lists(
    profile_names: list[str],
) -> tuple[list[str], list[str], list[str]]:
    """Merge selected profiles into haiku/sonnet/opus pack lists."""
    haiku: list[str] = []
    sonnet: list[str] = []
    opus: list[str] = []
    for name in profile_names:
        profile = PROFILES[name]
        haiku.extend(p for p in profile.get("haiku", []) if p not in haiku)
        sonnet.extend(p for p in profile.get("sonnet", []) if p not in sonnet)
        opus.extend(p for p in profile.get("opus", []) if p not in opus)
    return haiku, sonnet, opus


def preflight_check() -> bool:
    """Check if peon-ping is installed."""
    if not PEON_SH.is_file():
        print(f"ERROR: peon-ping not found at {PEON_DIR}")
        return False
    return True


def install_missing_packs(all_packs: list[str]):
    """Install all required packs if not already present."""
    print("--- Step 1: Installing missing packs ---")
    for pack in all_packs:
        pack_path = PEON_DIR / "packs" / pack
        if pack_path.is_dir():
            print(f"  [skip]    {pack}")
        else:
            print(f"  [install] {pack}")
            try:
                result = subprocess.run(
                    [str(PEON_SH), "packs", "install", pack],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                for line in result.stdout.split("\n"):
                    if any(x in line for x in ["[", "Warning", "Error"]):
                        print(f"    {line}")
            except subprocess.TimeoutExpired:
                print(f"    [timeout] {pack}")
    print()


def _mk_hook_model_pack(
    haiku_packs: list[str], sonnet_packs: list[str], opus_packs: list[str]
) -> str:
    """Generate the hook-model-pack.sh script content."""
    haiku_str = " ".join(haiku_packs)
    sonnet_str = " ".join(sonnet_packs)
    opus_str = " ".join(opus_packs)

    return f"""#!/bin/bash
# hook-model-pack.sh — SessionStart: pick random pack for the active model tier
# Managed by configure_claude.py — do not edit manually
set -euo pipefail

PEON_DIR="${{CLAUDE_CONFIG_DIR:-$HOME/.claude}}/hooks/peon-ping"
STATE="$PEON_DIR/.state.json"
SETTINGS="${{CLAUDE_CONFIG_DIR:-$HOME/.claude}}/settings.json"

HAIKU_PACKS=({haiku_str})
SONNET_PACKS=({sonnet_str})
OPUS_PACKS=({opus_str})

INPUT=$(cat)

SESSION_ID=$(echo "$INPUT" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get("session_id") or d.get("conversation_id") or "default")
except:
    print("default")
' 2>/dev/null || echo "default")

# Try model from hook JSON first, fall back to settings.json
MODEL=$(echo "$INPUT" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get("model", ""))
except:
    print("")
' 2>/dev/null || echo "")

if [ -z "$MODEL" ]; then
  MODEL=$(python3 -c "
import json
try:
    with open('$SETTINGS') as f:
        d = json.load(f)
    print(d.get('model', 'sonnet'))
except:
    print('sonnet')
" 2>/dev/null || echo "sonnet")
fi

MODEL_LOWER=$(echo "$MODEL" | tr '[:upper:]' '[:lower:]')
if echo "$MODEL_LOWER" | grep -q "haiku"; then
  POOL=("${{HAIKU_PACKS[@]}}")
elif echo "$MODEL_LOWER" | grep -q "opus"; then
  POOL=("${{OPUS_PACKS[@]}}")
else
  POOL=("${{SONNET_PACKS[@]}}")
fi

# Filter to installed packs only
INSTALLED=()
for p in "${{POOL[@]}}"; do
  [ -d "$PEON_DIR/packs/$p" ] && INSTALLED+=("$p")
done

[ ${{#INSTALLED[@]}} -eq 0 ] && exit 0

PACK="${{INSTALLED[$((RANDOM % ${{#INSTALLED[@]}}))]}}"

export PEON_ENV_STATE="$STATE" PEON_ENV_SESSION_ID="$SESSION_ID" PEON_ENV_PACK="$PACK" PEON_ENV_MODEL="$MODEL"
python3 << 'PYTHON_EOF'
import json, time, os
state_path = os.environ['PEON_ENV_STATE']
session_id = os.environ['PEON_ENV_SESSION_ID']
pack       = os.environ['PEON_ENV_PACK']
model      = os.environ['PEON_ENV_MODEL']
try:
    with open(state_path) as f:
        state = json.load(f)
except:
    state = dict()
state.setdefault('session_packs', dict())[session_id] = dict(pack=pack, last_used=time.time())
state['last_model'] = model
with open(state_path, 'w') as f:
    json.dump(state, f, indent=2)
    f.write('\\n')
PYTHON_EOF
exit 0
"""


def _mk_hook_model_switch(
    haiku_packs: list[str], sonnet_packs: list[str], opus_packs: list[str]
) -> str:
    """Generate the hook-model-switch.sh script content."""
    haiku_str = " ".join(haiku_packs)
    sonnet_str = " ".join(sonnet_packs)
    opus_str = " ".join(opus_packs)

    return f"""#!/bin/bash
# hook-model-switch.sh — UserPromptSubmit: detect model change and switch pack
# Managed by configure_claude.py — do not edit manually
set -euo pipefail

PEON_DIR="${{CLAUDE_CONFIG_DIR:-$HOME/.claude}}/hooks/peon-ping"
STATE="$PEON_DIR/.state.json"
SETTINGS="${{CLAUDE_CONFIG_DIR:-$HOME/.claude}}/settings.json"

HAIKU_PACKS=({haiku_str})
SONNET_PACKS=({sonnet_str})
OPUS_PACKS=({opus_str})

INPUT=$(cat)

SESSION_ID=$(echo "$INPUT" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get("session_id") or d.get("conversation_id") or "default")
except:
    print("default")
' 2>/dev/null || echo "default")

# Read current model from settings.json
CURRENT_MODEL=$(python3 -c "
import json
try:
    with open('$SETTINGS') as f:
        d = json.load(f)
    print(d.get('model', 'sonnet'))
except:
    print('sonnet')
" 2>/dev/null || echo "sonnet")

# Read last-known model from .state.json
LAST_MODEL=$(python3 -c "
import json
try:
    with open('$STATE') as f:
        d = json.load(f)
    print(d.get('last_model', ''))
except:
    print('')
" 2>/dev/null || echo "")

# Normalize both to tier
normalize_tier() {{
  local m
  m=$(echo "$1" | tr '[:upper:]' '[:lower:]')
  if echo "$m" | grep -q "haiku"; then echo "haiku"
  elif echo "$m" | grep -q "opus"; then echo "opus"
  else echo "sonnet"
  fi
}}

CURRENT_TIER=$(normalize_tier "$CURRENT_MODEL")
LAST_TIER=$(normalize_tier "$LAST_MODEL")

# No change — pass through
if [ "$CURRENT_TIER" = "$LAST_TIER" ] && [ -n "$LAST_MODEL" ]; then
  echo '{{"continue": true}}'
  exit 0
fi

# Model changed — pick a new pack from the right pool
case "$CURRENT_TIER" in
  haiku)  POOL=("${{HAIKU_PACKS[@]}}") ;;
  opus)   POOL=("${{OPUS_PACKS[@]}}") ;;
  *)      POOL=("${{SONNET_PACKS[@]}}") ;;
esac

INSTALLED=()
for p in "${{POOL[@]}}"; do
  [ -d "$PEON_DIR/packs/$p" ] && INSTALLED+=("$p")
done

if [ ${{#INSTALLED[@]}} -eq 0 ]; then
  echo '{{"continue": true}}'
  exit 0
fi

PACK="${{INSTALLED[$((RANDOM % ${{#INSTALLED[@]}}))]}}"

# Update .state.json: session pack + last_model
export PEON_ENV_STATE="$STATE" PEON_ENV_SESSION_ID="$SESSION_ID" PEON_ENV_PACK="$PACK" PEON_ENV_MODEL="$CURRENT_MODEL"
python3 << 'PYTHON_EOF'
import json, time, os
state_path = os.environ['PEON_ENV_STATE']
session_id = os.environ['PEON_ENV_SESSION_ID']
pack       = os.environ['PEON_ENV_PACK']
model      = os.environ['PEON_ENV_MODEL']
try:
    with open(state_path) as f:
        state = json.load(f)
except:
    state = dict()
state.setdefault('session_packs', dict())[session_id] = dict(pack=pack, last_used=time.time())
state['last_model'] = model
with open(state_path, 'w') as f:
    json.dump(state, f, indent=2)
    f.write('\\n')
PYTHON_EOF

# Trigger immediate notification sound with new pack (suppress output)
"$PEON_DIR/peon.sh" >/dev/null 2>&1 <<NOTIFY_EOF
{{
  "event_type": "notification",
  "session_id": "$SESSION_ID"
}}
NOTIFY_EOF

echo '{{"continue": true}}'
exit 0
"""


def create_hook_model_pack(
    haiku_packs: list[str], sonnet_packs: list[str], opus_packs: list[str]
):
    """Create hook-model-pack.sh for SessionStart event."""
    print("--- Step 2: Creating hook-model-pack.sh ---")

    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    hook_path = SCRIPTS_DIR / "hook-model-pack.sh"
    content = _mk_hook_model_pack(haiku_packs, sonnet_packs, opus_packs)
    if hook_path.is_file() and hook_path.read_text() == content:
        print(f"  [skip] {hook_path} already up to date")
    else:
        hook_path.write_text(content)
        hook_path.chmod(0o755)
        print(f"  Created: {hook_path}")
    print()


def create_hook_model_switch(
    haiku_packs: list[str], sonnet_packs: list[str], opus_packs: list[str]
):
    """Create hook-model-switch.sh for UserPromptSubmit event."""
    print("--- Step 3: Creating hook-model-switch.sh ---")

    hook_path = SCRIPTS_DIR / "hook-model-switch.sh"
    content = _mk_hook_model_switch(haiku_packs, sonnet_packs, opus_packs)
    if hook_path.is_file() and hook_path.read_text() == content:
        print(f"  [skip] {hook_path} already up to date")
    else:
        hook_path.write_text(content)
        hook_path.chmod(0o755)
        print(f"  Created: {hook_path}")
    print()


def patch_config_json():
    """Set pack_rotation_mode to session_override in config.json."""
    print("--- Step 4: Patching config.json ---")

    try:
        with open(CONFIG) as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        config = {}

    config["pack_rotation_mode"] = "session_override"

    with open(CONFIG, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    print("  pack_rotation_mode = session_override")
    print()


def patch_settings_json():
    """Patch settings.json to add peon-ping hooks."""
    print("--- Step 5: Patching settings.json ---")

    # On WSL, Claude Code's sandbox blocks powershell.exe which the "wsl"
    # audio path requires.  Force PLATFORM=linux so peon uses paplay/ffplay
    # via PulseAudio (WSLg) instead.
    prefix = "PLATFORM=linux " if _is_wsl() else ""
    hook_pack = prefix + str(SCRIPTS_DIR / "hook-model-pack.sh")
    hook_switch = prefix + str(SCRIPTS_DIR / "hook-model-switch.sh")
    peon_sh = prefix + str(PEON_SH)

    try:
        with open(SETTINGS_JSON) as f:
            settings = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        settings = {}

    settings.setdefault("hooks", {})

    def has_command(entries: list, cmd: str) -> bool:
        """Check if command already exists in hook entries.

        Normalizes $HOME and ~ to the real home dir before comparing,
        so absolute paths and $HOME-prefixed paths don't create duplicates.
        """
        home = str(Path.home())

        def normalize(s: str) -> str:
            s = s.replace("PLATFORM=linux ", "")
            return s.replace("$HOME", home).replace("~/", home + "/")

        cmd_norm = normalize(cmd)
        return any(
            any(
                normalize(h.get("command", "")) == cmd_norm
                for h in entry.get("hooks", [])
            )
            for entry in entries
        )

    def ensure_peon(entries: list, label: str):
        """Ensure peon.sh is registered in hook entries."""
        if not has_command(entries, peon_sh):
            entries.append(
                {"hooks": [{"type": "command", "command": peon_sh, "timeout": 10}]}
            )
            print(f"  Added peon.sh to {label}")
        else:
            print(f"  [skip] peon.sh already in {label}")

    # SessionStart: insert hook-model-pack first, then peon.sh
    ss = settings["hooks"].setdefault("SessionStart", [])
    if not has_command(ss, hook_pack):
        ss.insert(
            0,
            {
                "matcher": "",
                "hooks": [{"type": "command", "command": hook_pack, "timeout": 10}],
            },
        )
        print("  Added hook-model-pack.sh to SessionStart")
    else:
        print("  [skip] hook-model-pack.sh already in SessionStart")
    ensure_peon(ss, "SessionStart")

    # UserPromptSubmit: append hook-model-switch
    up = settings["hooks"].setdefault("UserPromptSubmit", [])
    if not has_command(up, hook_switch):
        up.append(
            {
                "matcher": "",
                "hooks": [{"type": "command", "command": hook_switch, "timeout": 5}],
            }
        )
        print("  Added hook-model-switch.sh to UserPromptSubmit")
    else:
        print("  [skip] hook-model-switch.sh already in UserPromptSubmit")

    # Sound events: ensure peon.sh is registered
    for event in ("Stop", "PermissionRequest", "Notification", "PostToolUseFailure"):
        entries = settings["hooks"].setdefault(event, [])
        ensure_peon(entries, event)

    with open(SETTINGS_JSON, "w") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")

    print()


def print_summary(
    profile_names: list[str],
    haiku_packs: list[str],
    sonnet_packs: list[str],
    opus_packs: list[str],
):
    """Print configuration summary."""
    print("=== Done ===")
    print()
    print(f"  profiles: {', '.join(profile_names)}")
    print(f"  haiku  ({len(haiku_packs)} packs): {' '.join(haiku_packs)}")
    print(f"  sonnet ({len(sonnet_packs)} packs): {' '.join(sonnet_packs)}")
    print(f"  opus   ({len(opus_packs)} packs):  {' '.join(opus_packs)}")
    print()
    print("Restart Claude Code to activate.")


def main():
    # --list-profiles flag for quick reference
    if "--list-profiles" in sys.argv:
        print("Available peon-ping profiles:")
        for name, profile in sorted(PROFILES.items()):
            total = sum(len(profile.get(t, [])) for t in ("haiku", "sonnet", "opus"))
            print(f"  {name:<16s} {total:>3d} packs")
        return

    profile_names = resolve_profiles()

    print("=== Peon-Ping Model Pack Configuration ===")
    print(f"Location: {PEON_DIR}")
    print(f"Profiles: {', '.join(profile_names)}")
    print()

    if not preflight_check():
        sys.exit(1)

    haiku_packs, sonnet_packs, opus_packs = build_tier_lists(profile_names)
    all_packs = haiku_packs + sonnet_packs + opus_packs

    install_missing_packs(all_packs)
    create_hook_model_pack(haiku_packs, sonnet_packs, opus_packs)
    create_hook_model_switch(haiku_packs, sonnet_packs, opus_packs)
    patch_config_json()
    patch_settings_json()
    print_summary(profile_names, haiku_packs, sonnet_packs, opus_packs)


if __name__ == "__main__":
    main()
