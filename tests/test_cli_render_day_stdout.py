from __future__ import annotations

from datetime import date, datetime

from typer.testing import CliRunner

from chronotes.cli.main import app
from chronotes.domain.models import DailyPageData, DayMarkers
from chronotes.domain.planets import SUN
from chronotes.render.latex_render import render_day_page
from chronotes.services.planetary_hours import build_planetary_hours
from chronotes.services.sun_sign import sun_sign_for_day

runner = CliRunner()


def test_cli_render_day_stdout_matches_renderer() -> None:
    markers = DayMarkers(
        sunrise=datetime.fromisoformat("2026-01-27T07:55:00"),
        solar_noon=datetime.fromisoformat("2026-01-27T13:20:00"),
        sunset=datetime.fromisoformat("2026-01-27T17:45:00"),
        next_sunrise=datetime.fromisoformat("2026-01-28T07:54:00"),
    )

    hours = build_planetary_hours(day_ruler=SUN, markers=markers)
    sun_sign = sun_sign_for_day(date(2026, 1, 23))
    expected = render_day_page(
        DailyPageData(
            city="Indianapolis",
            day=date.fromisoformat("2026-01-27"),
            day_ruler=SUN,
            moon_phase="Waxing Crescent",
            markers=markers,
            hours=hours,
            sun_sign=sun_sign
        )
    )

    result = runner.invoke(
        app,
        [
            "render-day",
            "--city",
            "Indianapolis",
            "--day",
            "2026-01-27",
            "--day-ruler-key",
            "sun",
            "--moon-phase",
            "Waxing Crescent",
            "--sunrise",
            "2026-01-27T07:55:00",
            "--solar-noon",
            "2026-01-27T13:20:00",
            "--sunset",
            "2026-01-27T17:45:00",
            "--next-sunrise",
            "2026-01-28T07:54:00",
        ],
    )

    assert result.exit_code == 0, result.stdout
    assert result.stdout == expected + "\n"
