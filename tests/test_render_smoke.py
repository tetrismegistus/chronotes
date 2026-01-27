from __future__ import annotations

from datetime import date, datetime, timezone

from chronotes.domain.models import DailyPageData, DayMarkers, PlanetaryHour, PlanetaryHours
from chronotes.domain.planets import SATURN, SUN
from chronotes.render.latex_render import render_day_page


def test_render_day_page_smoke_contains_key_fields() -> None:
    tz = timezone.utc
    markers = DayMarkers(
        sunrise=datetime(2026, 1, 27, 12, 0, tzinfo=tz),
        solar_noon=datetime(2026, 1, 27, 18, 0, tzinfo=tz),
        sunset=datetime(2026, 1, 27, 22, 0, tzinfo=tz),
        next_sunrise=datetime(2026, 1, 28, 12, 1, tzinfo=tz),
    )

    # Smoke test: renderer shouldn't care that these aren't 12/12;
    # cardinality is service-layer responsibility (already tested elsewhere).
    day_hours = (PlanetaryHour(ruler=SATURN, start=markers.sunrise, end=markers.solar_noon),)
    night_hours = (PlanetaryHour(ruler=SUN, start=markers.sunset, end=markers.next_sunrise),)

    data = DailyPageData(
        city="Indianapolis, IN",
        day=date(2026, 1, 27),
        day_ruler=SUN,
        moon_phase="Waxing Crescent",
        markers=markers,
        hours=PlanetaryHours(day=day_hours, night=night_hours),
    )

    tex = render_day_page(data)

    assert "Indianapolis, IN" in tex
    assert "2026-01-27" in tex
    assert "Planetary Hours" in tex
    assert "Solar Noon: 18:00" in tex
    assert "Waxing Crescent" in tex
    assert "Sun" in tex
    assert "Saturn" in tex
