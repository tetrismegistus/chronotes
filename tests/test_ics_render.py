from __future__ import annotations

from datetime import date, datetime, timezone

from chronotes.domain.models import DailyPageData, DayMarkers
from chronotes.domain.planets import SUN
from chronotes.render.ics_render import render_calendar_from_days
from chronotes.services.planetary_hours import build_planetary_hours


def _mk_day() -> DailyPageData:
    sunrise = datetime(2026, 1, 1, 7, 0, 0, tzinfo=timezone.utc)
    solar_noon = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    sunset = datetime(2026, 1, 1, 17, 0, 0, tzinfo=timezone.utc)
    next_sunrise = datetime(2026, 1, 2, 7, 0, 0, tzinfo=timezone.utc)

    markers = DayMarkers(
        sunrise=sunrise,
        solar_noon=solar_noon,
        sunset=sunset,
        next_sunrise=next_sunrise,
    )
    hours = build_planetary_hours(day_ruler=SUN, markers=markers)

    return DailyPageData(
        city="Indianapolis, IN; USA",
        day=date(2026, 1, 1),
        day_ruler=SUN,
        moon_phase="Waxing Crescent",
        markers=markers,
        hours=hours,
        sun_sign=None,
    )


def test_render_calendar_has_expected_envelope_and_event_count() -> None:
    day = _mk_day()
    dtstamp = datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    ics = render_calendar_from_days([day], dtstamp=dtstamp)

    assert "BEGIN:VCALENDAR" in ics
    assert "END:VCALENDAR" in ics
    assert ics.count("BEGIN:VEVENT") == 24
    assert ics.count("END:VEVENT") == 24
