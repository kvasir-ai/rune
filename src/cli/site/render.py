"""Jinja rendering helpers for the documentation site."""
from __future__ import annotations

from jinja2 import Environment, PackageLoader, select_autoescape

_ENV = Environment(
    loader=PackageLoader("cli.site", "templates"),
    autoescape=select_autoescape(("html", "xml")),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_template(template_name: str, **context: object) -> str:
    """Render a packaged Jinja template."""
    return _ENV.get_template(template_name).render(**context)
