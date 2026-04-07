"""Shared helpers for section chrome."""

from __future__ import annotations

from ..catalog.html import breadcrumb_html, stage_progress_html


def page_nav(items: list[str | tuple[str, str]], stage: int | None = None) -> str:
    """Render the shared breadcrumb and optional stage-progress chrome."""
    parts = [breadcrumb_html(items)]
    if stage is not None:
        parts.append(stage_progress_html(stage))
    return "\n".join(parts)
