from __future__ import annotations

from dataclasses import asdict, is_dataclass
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from chronotes.domain.models import DailyPageData


def _default_templates_dir() -> Path:
    return Path(__file__).resolve().parent / "templates"


def _fmt_time(dt) -> str:
    # Avoid timezone surprises in tests: format is stable.
    return dt.strftime("%H:%M")


def _fmt_date(d) -> str:
    return d.isoformat()


def render_day_page(data: DailyPageData, *, templates_dir: Path | None = None) -> str:
    """
    Indicates: pure transformation (domain -> LaTeX string).
    No filesystem writes, no PDF compilation.
    """
    tdir = templates_dir or _default_templates_dir()
    env = Environment(
        loader=FileSystemLoader(str(tdir)),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["fmt_time"] = _fmt_time
    env.filters["fmt_date"] = _fmt_date

    template = env.get_template("pagetemplate.tex.j2")

    return template.render(data=data)


def render_document(pages: list[str], *, templates_dir: Path | None = None) -> str:
    """
    Pure wrapper: pages (already-rendered LaTeX fragments) -> full LaTeX document.
    """
    tdir = templates_dir or _default_templates_dir()
    env = Environment(
        loader=FileSystemLoader(str(tdir)),
        undefined=StrictUndefined,
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("doctemplate.tex.j2")
    body = "\n".join(pages)
    return template.render(body=body)


def render_document_from_days(
    days: Sequence[DailyPageData], *, templates_dir: Path | None = None
) -> str:
    """
    Pure convenience: DailyPageData[] -> full LaTeX document.
    Renders each day page via pagetemplate, then wraps via doctemplate.
    """
    pages = [render_day_page(d, templates_dir=templates_dir) for d in days]
    return render_document(pages, templates_dir=templates_dir)
