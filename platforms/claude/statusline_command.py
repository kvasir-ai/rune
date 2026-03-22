#!/usr/bin/env python3
"""Claude Code status line — configurable via statusline.yaml."""

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

# ── ANSI colors ──────────────────────────────────────────────────────────────

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
ORANGE = "\033[38;5;208m"

SEP = f" {DIM}|{RESET} "

# ── Git cache ────────────────────────────────────────────────────────────────

GIT_CACHE_MAX_AGE = 5  # seconds


def _git_cache_path(cwd: str) -> Path:
    """Return a cache path keyed by the working directory to avoid cross-repo collisions."""
    key = hashlib.sha1(cwd.encode()).hexdigest()[:12]
    return Path(f"/tmp/statusline-git-cache-{key}")


def get_git_branch(cwd: str) -> str:
    """Get current git branch, cached to avoid subprocess on every update."""
    cache_path = _git_cache_path(cwd)
    try:
        if cache_path.exists():
            age = time.time() - cache_path.stat().st_mtime
            if age < GIT_CACHE_MAX_AGE:
                return cache_path.read_text().strip()

        result = subprocess.run(
            ["git", "-C", cwd, "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=1,
        )
        branch = result.stdout.strip() if result.returncode == 0 else ""

        # Fallback to short hash for detached HEAD
        if not branch:
            result = subprocess.run(
                ["git", "-C", cwd, "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                timeout=1,
            )
            branch = result.stdout.strip() if result.returncode == 0 else ""

        cache_path.write_text(branch)
        return branch
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return ""


# ── Config ───────────────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "directory": True,
    "git_branch": True,
    "gcloud_config": True,
    "model": True,
    "context_bar": True,
    "cost": True,
    "duration": True,
    "session_id": False,
    "vim_mode": True,
    "agent_name": True,
    "worktree": True,
}


def load_config() -> dict:
    """Load statusline.yaml from the same directory as this script."""
    config_path = Path(__file__).parent / "statusline.yaml"
    if not config_path.exists():
        return DEFAULT_CONFIG

    try:
        # Minimal YAML parser — config is flat key: bool, no dependency needed
        config = dict(DEFAULT_CONFIG)
        for line in config_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().lower()
            if key in DEFAULT_CONFIG:
                config[key] = value == "true"
        return config
    except OSError:
        return DEFAULT_CONFIG


# ── Segment builders ─────────────────────────────────────────────────────────


def get_gcloud_config() -> str:
    """Read active gcloud config name (file read, no subprocess)."""
    try:
        return (
            (Path.home() / ".config" / "gcloud" / "active_config").read_text().strip()
        )
    except (FileNotFoundError, OSError):
        return ""


def build_context_bar(pct: int) -> str:
    """Build a color-coded 10-cell progress bar."""
    if pct >= 90:
        color = RED
    elif pct >= 70:
        color = ORANGE
    else:
        color = GREEN

    filled = pct // 10
    bar = "█" * filled + "░" * (10 - filled)
    return f"{color}{bar}{RESET} {pct}%"


def format_duration(ms: int) -> str:
    """Format milliseconds as Xm Ys."""
    mins = ms // 60000
    secs = (ms % 60000) // 1000
    return f"{mins}m {secs}s"


# ── Main ─────────────────────────────────────────────────────────────────────


def build_status_lines(data: dict, cfg: dict) -> list[str]:
    """Build status line(s) from session data and config."""
    cwd = data.get("workspace", {}).get("current_dir") or data.get("cwd", "")
    cw = data.get("context_window") or {}
    cost = data.get("cost") or {}

    # ── Line 1: location and identity ────────────────────────────────────

    parts: list[str] = []

    if cfg["directory"] and cwd:
        parts.append(f"{CYAN}{Path(cwd).name}{RESET}")

    if cfg["git_branch"]:
        # Prefer worktree branch from session data (no subprocess needed)
        branch = data.get("worktree", {}).get("branch", "") or get_git_branch(cwd)
        if branch:
            parts.append(f"{DIM}on{RESET} {BLUE}{branch}{RESET}")

    if cfg["gcloud_config"]:
        gc = get_gcloud_config()
        if gc:
            parts.append(f"{YELLOW}{gc}{RESET}")

    if cfg["model"]:
        model = data.get("model", {})
        name = (
            model.get("display_name") or model.get("id", "")
            if isinstance(model, dict)
            else str(model)
        )
        if name:
            parts.append(f"{GREEN}{name}{RESET}")

    # Optional trailing segments on line 1
    if cfg["agent_name"]:
        agent = data.get("agent", {}).get("name", "")
        if agent:
            parts.append(f"{CYAN}agent:{agent}{RESET}")

    if cfg["worktree"]:
        wt = data.get("worktree", {})
        wt_name = wt.get("name", "")
        if wt_name:
            label = wt.get("branch", "") or wt_name
            parts.append(f"{DIM}wt:{RESET}{BLUE}{label}{RESET}")

    if cfg["session_id"]:
        sid = data.get("session_id", "")
        if sid:
            parts.append(f"{DIM}{sid[:8]}{RESET}")

    if cfg["vim_mode"]:
        vim = data.get("vim", {}).get("mode", "")
        if vim == "NORMAL":
            parts.append(f"{BOLD}{YELLOW}[N]{RESET}")
        elif vim == "INSERT":
            parts.append(f"{BOLD}{GREEN}[I]{RESET}")

    lines = [SEP.join(parts)] if parts else []

    # ── Line 2: metrics (only if any metric feature is enabled) ──────────

    metrics: list[str] = []

    if cfg["context_bar"]:
        pct = cw.get("used_percentage")
        if pct is not None:
            metrics.append(build_context_bar(int(pct)))

    if cfg["cost"]:
        usd = cost.get("total_cost_usd")
        if usd is not None:
            metrics.append(f"{YELLOW}${usd:.2f}{RESET}")

    if cfg["duration"]:
        ms = cost.get("total_duration_ms")
        if ms is not None:
            metrics.append(f"⏱ {format_duration(int(ms))}")

    if metrics:
        lines.append(SEP.join(metrics))

    return lines


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        data = {}

    cfg = load_config()
    lines = build_status_lines(data, cfg)

    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
