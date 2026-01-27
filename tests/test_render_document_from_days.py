from __future__ import annotations

from datetime import date, datetime, timezone

from chronotes.domain.models import DailyPageData, DayMarkers, PlanetaryHour, PlanetaryHours
from chronotes.domain.planets import SATURN, SUN
from chronotes.render.latex_render import render_document_from_days


def _page(city: str, d: date) -> DailyPageData:
    tz = timezone.utc
    markers = DayMarkers(
        sunrise=datetime(2026, 1, 27, 12, 0, tzinfo=tz),
        solar_noon=datetime(2026, 1, 27, 18, 0, tzinfo=tz),
        sunset=datetime(2026, 1, 27, 22, 0, tzinfo=tz),
        next_sunrise=datetime(2026, 1, 28, 12, 1, tzinfo=tz),
    )
    day_hours = (PlanetaryHour(ruler=SATURN, start=markers.sunrise, end=markers.solar_noon),)
    night_hours = (PlanetaryHour(ruler=SUN, start=markers.sunset, end=markers.next_sunrise),)

    return DailyPageData(
        city=city,
        day=d,
        day_ruler=SUN,
        moon_phase="Waxing Crescent",
        markers=markers,
        hours=PlanetaryHours(day=day_hours, night=night_hours),
    )


def test_render_document_from_days_preserves_order_and_count() -> None:
    a = _page("City A", date(2026, 1, 27))
    b = _page("City B", date(2026, 1, 28))

    tex = render_document_from_days([a, b])

    assert "City A" in tex
    assert "City B" in tex
    assert tex.index("City A") < tex.index("City B")

    # "Planetary Hours" appears once per page template render
    assert tex.count("Planetary Hours") == 2
