from __future__ import annotations

from datetime import date, datetime

import typer

from typing import Optional

from chronotes.domain.models import DailyPageData, DayMarkers
from chronotes.domain.planets import BY_KEY
from chronotes.render.latex_render import render_day_page
from chronotes.services.planetary_hours import build_planetary_hours
from chronotes.providers.geocode_nominatim import NominatimGeocodeProvider
from chronotes.services.location_resolution import resolve_location
from chronotes.providers.astronomy_astral import AstralDayMarkersProvider
from chronotes.providers.contracts import GeoPoint
from chronotes.providers.moon_phase_simple import SimpleMoonPhaseProvider
from chronotes.render.latex_render import render_document_from_days
from chronotes.services.day_builder import BuildContext, build_range
from chronotes.services.date_ranges import year_bounds
from chronotes.services.sun_sign import sun_sign_for_day


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
    sun_sign = sun_sign_for_day(day_date)
    data = DailyPageData(
        city=city,
        day=day_date,
        day_ruler=planet,
        moon_phase=moon_phase,
        markers=markers,
        hours=hours,
        sun_sign=sun_sign
    )

    typer.echo(render_day_page(data))


@app.command("render-range")
def render_range(
    *,
    city: Optional[str] = typer.Option(None),
    tz: str = typer.Option(..., help="IANA timezone, e.g. America/Indiana/Indianapolis"),
    lat: Optional[float] = typer.Option(None),
    lon: Optional[float] = typer.Option(None),
    user_agent: Optional[str] = typer.Option(None, "--user-agent", help="User-Agent for geocoding (required when using --city without --lat/--lon)."),
    start: str = typer.Option(..., help="ISO date, e.g. 2026-01-01"),
    end: str = typer.Option(..., help="ISO date, e.g. 2026-12-31"),
) -> None:
    start_d = _parse_date(start)
    end_d = _parse_date(end)

    geocoder = None
    geocoder = NominatimGeocodeProvider(user_agent=user_agent)

    try:
        loc = resolve_location(city=city, lat=lat, lon=lon, geocoder=geocoder)
    except ValueError as e:
        raise typer.BadParameter(str(e)) from e

    ctx = BuildContext(city=loc.city_label, point=loc.point, tz=tz)

    days = build_range(
        ctx=ctx,
        start=start_d,
        end=end_d,
        markers_provider=AstralDayMarkersProvider(),
        moon_provider=SimpleMoonPhaseProvider(),
    )
    typer.echo(render_document_from_days(days))


from typing import Optional

from chronotes.providers.geocode_nominatim import NominatimGeocodeProvider
from chronotes.services.location_resolution import resolve_location


@app.command("render-year")
def render_year(
    *,
    city: Optional[str] = typer.Option(
        None,
        help="City label to print; if no --lat/--lon are provided, this is also the geocoding query.",
    ),
    tz: str = typer.Option(..., help="IANA timezone, e.g. America/Indiana/Indianapolis"),
    lat: Optional[float] = typer.Option(
        None,
        help="Latitude (optional). If provided, --lon is required. Overrides geocoding.",
    ),
    lon: Optional[float] = typer.Option(
        None,
        help="Longitude (optional). If provided, --lat is required. Overrides geocoding.",
    ),
    user_agent: Optional[str] = typer.Option(
        None,
        "--user-agent",
        help="User-Agent for Nominatim (required when using --city without coords).",
    ),
    year: int = typer.Option(..., help="Year, e.g. 2026"),
) -> None:
    start_d, end_d = year_bounds(year)

    # Implicit geocoding: if coords are not provided and city is provided, geocode.
    geocoder = None
    if lat is None and lon is None and city:
        if not user_agent:
            raise typer.BadParameter(
                "--user-agent is required when using --city without --lat/--lon."
            )
        geocoder = NominatimGeocodeProvider(user_agent=user_agent)

    try:
        loc = resolve_location(city=city, lat=lat, lon=lon, geocoder=geocoder)
    except ValueError as e:
        raise typer.BadParameter(str(e)) from e

    ctx = BuildContext(city=loc.city_label, point=loc.point, tz=tz)

    days = build_range(
        ctx=ctx,
        start=start_d,
        end=end_d,
        markers_provider=AstralDayMarkersProvider(),
        moon_provider=SimpleMoonPhaseProvider(),
    )

    typer.echo(render_document_from_days(days))



def main() -> None:
    app()


if __name__ == "__main__":
    main()

