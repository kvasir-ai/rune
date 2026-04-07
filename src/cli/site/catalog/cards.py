"""Catalog card renderers for agents, skills, and rules."""

from __future__ import annotations

from .html import esc

_PHASE_ORDER = ["explore", "plan", "build", "validate", "general"]
_PHASE_LABELS = {
    "explore": "🔍 Explore",
    "plan": "📐 Plan",
    "build": "🔨 Build",
    "validate": "✅ Validate",
    "general": "🌐 General",
}

_COLOR_MAP = {
    "red": "#b91c1c",
    "orange": "#f97316",
    "yellow": "#eab308",
    "gold": "#d97706",
    "green": "#3d6b3b",
    "teal": "#14b8a6",
    "cyan": "#06b6d4",
    "blue": "#2563eb",
    "indigo": "#4f46e5",
    "violet": "#7c3aed",
    "purple": "#9333ea",
    "pink": "#db2777",
    "gray": "#4b5563",
    "white": "#f3f4f6",
}


def _truncate(text: str, length: int, split_on: str = " ") -> str:
    if len(text) <= length:
        return text
    return text[:length].rsplit(split_on, 1)[0] + "\u2026"


def _phase_groups(items: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for item in items:
        phase = item.get("phase") or "general"
        grouped.setdefault(phase, []).append(item)
    return grouped


def _render_simple_catalog(
    categories: dict[str, list[dict]],
    github_blob: str,
    *,
    title_html,
    desc_key: str = "description",
    emoji_html,
    aria_label,
) -> str:
    by_phase: dict[str, list[dict]] = {}
    for category in sorted(categories):
        for item in categories[category]:
            phase = item.get("phase") or "general"
            by_phase.setdefault(phase, []).append(item)

    parts = []
    for phase in _PHASE_ORDER:
        if phase not in by_phase:
            continue
        parts.append('<section class="phase-group">')
        parts.append(
            f'<div class="phase-label phase-{esc(phase)}">{_PHASE_LABELS[phase]}</div>'
        )
        parts.append('<div class="card-grid">')
        for item in by_phase[phase]:
            desc = _truncate(item[desc_key], 90)
            gh_url = f"{github_blob}/{item['rel_path']}"
            parts.append(
                f'<a href="{esc(gh_url)}" target="_blank" rel="noopener" '
                f'class="resource-link" aria-label="{esc(aria_label(item))}">'
                f'<div class="card">'
                f'<span class="emoji" aria-hidden="true">{emoji_html(item)}</span>'
                f"<h4>{title_html(item)}</h4>"
                f"<p>{esc(desc)}</p>"
                f"</div></a>"
            )
        parts.append("</div></section>")
    return "\n".join(parts)


def _agent_card(agent: dict, github_blob: str) -> str:
    emoji = agent["emoji"] or "&#x1F916;"
    model_tag = f'<span class="tag">{esc(agent["model"])}</span>' if agent["model"] else ""
    version_tag = (
        f'<span class="tag tag-version">{esc(agent["version"])}</span>'
        if agent.get("version")
        else ""
    )
    desc = _truncate(agent["description"], 100)
    tools = agent.get("tools", "")
    tools_html = ""
    if tools:
        tools_html = f'<p class="agent-tools">{esc(_truncate(tools, 55, ","))}</p>'
    color = agent.get("color", "")
    border_style = (
        f' style="border-top-color:{_COLOR_MAP.get(color, "var(--border)")}"'
        if color
        else ""
    )
    gh_url = f"{github_blob}/{agent['rel_path']}"
    return f"""<a href="{esc(gh_url)}" target="_blank" rel="noopener" class="resource-link" aria-label="View {esc(agent["name"])} on GitHub">
  <div class="agent-card"{border_style}>
    <span class="agent-emoji" aria-hidden="true">{emoji}</span>
    <div class="agent-info">
      <h4>{esc(agent["name"])}</h4>
      <p>{esc(desc)}</p>
      {tools_html}
      {model_tag}{version_tag}
    </div>
  </div>
</a>"""


def agent_grid(categories: dict[str, list[dict]], github_blob: str) -> str:
    """Generate agent card grid HTML."""
    parts = []
    by_phase_and_category: dict[str, dict[str, list[dict]]] = {}
    for category, items in categories.items():
        for phase, phase_items in _phase_groups(items).items():
            by_phase_and_category.setdefault(phase, {})[category] = phase_items

    for phase in _PHASE_ORDER:
        phase_categories = by_phase_and_category.get(phase)
        if not phase_categories:
            continue
        parts.append('<section class="phase-group">')
        parts.append(
            f'<div class="phase-label phase-{esc(phase)}">{_PHASE_LABELS[phase]}</div>'
        )
        for category in sorted(phase_categories):
            parts.append('<div class="agent-grid">')
            for agent in phase_categories[category]:
                parts.append(_agent_card(agent, github_blob))
            parts.append("</div>")
        parts.append("</section>")
    return "\n".join(parts)


def skill_table(categories: dict[str, list[dict]], github_blob: str) -> str:
    """Generate skill catalog grid."""
    return _render_simple_catalog(
        categories,
        github_blob,
        title_html=lambda item: f"<code>/{esc(item['name'])}</code>",
        emoji_html=lambda item: item.get("emoji") or "&#x1F4DD;",
        aria_label=lambda item: f"View /{item['name']} skill on GitHub",
    )


def rules_section(categories: dict[str, list[dict]], github_blob: str) -> str:
    """Generate rules catalog grid."""
    return _render_simple_catalog(
        categories,
        github_blob,
        title_html=lambda item: esc(item["name"]),
        emoji_html=lambda _item: "&#x1F4DA;",
        aria_label=lambda item: f"View {item['name']} rule on GitHub",
    )
