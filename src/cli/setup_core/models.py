from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

RESOURCE_CATEGORIES = ("core", "explore", "plan", "build", "validate")
PROFILE_CONTENT_KEYS = ("agents", "rules", "skills", "hooks", "mcps")


@dataclass
class AvailableContent:
    """Available resources in the agency directory."""

    agents: dict[str, list[str]] = field(default_factory=dict)
    rules: dict[str, list[str]] = field(default_factory=dict)
    skills: list[str] = field(default_factory=list)
    hooks: list[str] = field(default_factory=list)
    mcps: list[str] = field(default_factory=list)


@dataclass
class Tool:
    """System tool registration and status."""

    name: str
    binary: str
    description: str
    installed: bool
    required: bool = False
    check: str | None = None


@dataclass
class Selections:
    """Selected resources for a profile."""

    based_on: str | None = None
    active_name: str | None = None
    base_hash: str | None = None
    agents: dict[str, list[str]] = field(default_factory=dict)
    rules: dict[str, list[str]] = field(default_factory=dict)
    skills: list[str] = field(default_factory=list)
    hooks: list[str] = field(default_factory=list)
    mcps: list[str] = field(default_factory=list)


@dataclass
class CurrentState:
    """Current installation state and drift status."""

    status: Literal["none", "profile"]
    profile_name: str | None = None
    selections: Selections | None = None
    base_stale: bool = False
    content_stale: bool = False
