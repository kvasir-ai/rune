"""Small HTML helpers for the static site generator."""

from __future__ import annotations

import html as _html


def esc(value: str) -> str:
    """Escape HTML content for safe inline rendering."""
    return _html.escape(value)


def breadcrumb_html(items: list[str | tuple[str, str]]) -> str:
    """Render a breadcrumb trail from plain labels and section links."""
    crumbs = []
    for item in items:
        if isinstance(item, tuple):
            section, label = item
            crumbs.append(f'<button data-section="{esc(section)}">{esc(label)}</button>')
        else:
            crumbs.append(esc(item))
    return (
        '  <nav class="breadcrumb" aria-label="Breadcrumb">'
        + " <span>&#x203A;</span> ".join(crumbs)
        + "</nav>"
    )


def stage_progress_html(current: int) -> str:
    """Render the shared four-stage progress control."""
    labels = {1: "Orientation", 2: "First Run", 3: "Customize", 4: "Mastery"}
    steps = []
    for step, label in labels.items():
        active = " active" if step == current else ""
        expanded = "true" if step == current else "false"
        steps.append(
            f'    <button class="stage-progress-step stage-{step}{active}" '
            f'data-stage-nav="{step}" aria-expanded="{expanded}">{step} &middot; {label}</button>'
        )
    return (
        f'  <nav class="stage-progress" data-current-stage="{current}" aria-label="Stage progress">\n'
        + "\n".join(steps)
        + "\n  </nav>"
    )
