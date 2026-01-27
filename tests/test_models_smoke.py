from datetime import datetime, date, timezone, timedelta

from chronotes.domain.models import (
    DayMarkers,
    PlanetaryHour,
    PlanetaryHours,
    DailyPageData,
)
from chronotes.domain.planets import SUN


def test_daily_page_data_constructible():
    t0 = datetime(2026, 1, 27, 7, 0, tzinfo=timezone.utc)

    markers = DayMarkers(
        sunrise=t0,
        solar_noon=t0 + timedelta(hours=5),
        sunset=t0 + timedelta(hours=10),
        next_sunrise=t0 + timedelta(days=1),
    )

    hour = PlanetaryHour(
        ruler=SUN,
        start=t0,
        end=t0 + timedelta(minutes=60),
    )

    hours = PlanetaryHours(
        day=(hour,) * 12,
        night=(hour,) * 12,
    )

    page = DailyPageData(
        city="Indianapolis, IN",
        day=date(2026, 1, 27),
        day_ruler=SUN,
        moon_phase="Full",
        markers=markers,
        hours=hours,
    )

    assert page.city == "Indianapolis, IN"
    assert len(page.hours.day) == 12
    assert page.hours.day[0].ruler.key == "sun"
