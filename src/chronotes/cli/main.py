from __future__ import annotations

from datetime import date, datetime

import typer

from chronotes.domain.models import DailyPageData, DayMarkers
from chronotes.domain.planets import BY_KEY
from chronotes.render.latex_render import render_day_page
from chronotes.services.planetary_hours import build_planetary_hours

app = typer.Typer(no_args_is_help=True)


@app.callback()
def _root() -> None:
    """chronotes CLI."""


@app.command()
def hello() -> None:
    """Sanity check command."""
    typer.echo("chronotes: ok")


def _parse_dt(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value)
    except ValueError as e:
        raise typer.BadParameter(
            "Expected ISO datetime like 2026-01-27T07:55:00 (seconds optional)."
        ) from e


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as e:
        raise typer.BadParameter("Expected ISO date like 2026-01-27.") from e


@app.command("render-day")
def render_day(
    *,
    city: str = typer.Option(..., help="City label to print on the page."),
    day: str = typer.Option(..., help="ISO date, e.g. 2026-01-27."),
    day_ruler_key: str = typer.Option(
        ...,
        "--day-ruler-key",
        help="Planet key (explicit to avoid weekday-index ambiguity).",
    ),
    moon_phase: str = typer.Option(..., help="Moon phase label to print."),
    sunrise: str = typer.Option(..., help="ISO datetime, e.g. 2026-01-27T07:55:00"),
    solar_noon: str = typer.Option(..., help="ISO datetime, e.g. 2026-01-27T13:20:00"),
    sunset: str = typer.Option(..., help="ISO datetime, e.g. 2026-01-27T17:45:00"),
    next_sunrise: str = typer.Option(..., help="ISO datetime, e.g. 2026-01-28T07:54:00"),
) -> None:
    """
    Render a single daily LaTeX page to stdout from explicit markers.
    No filesystem output. No providers.
    """
    planet = BY_KEY.get(day_ruler_key)
    if planet is None:
        raise typer.BadParameter(
            f"Unknown planet key: {day_ruler_key}. Choices: {', '.join(BY_KEY)}"
        )

    day_date = _parse_date(day)

    markers = DayMarkers(
        sunrise=_parse_dt(sunrise),
        solar_noon=_parse_dt(solar_noon),
        sunset=_parse_dt(sunset),
        next_sunrise=_parse_dt(next_sunrise),
    )

    hours = build_planetary_hours(day_ruler=planet, markers=markers)

    data = DailyPageData(
        city=city,
        day=day_date,
        day_ruler=planet,
        moon_phase=moon_phase,
        markers=markers,
        hours=hours,
    )

    typer.echo(render_day_page(data))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
