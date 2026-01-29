from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from chronotes.domain.models import DayMarkers
from chronotes.providers.contracts import DayMarkersProvider, GeoPoint, MoonPhaseProvider
from chronotes.services.day_builder import BuildContext, build_range
from chronotes.domain.sunsigns import CAPRICORN

class FakeMarkers(DayMarkersProvider):
    def get_markers(self, *, day: date, point: GeoPoint, tz: str) -> DayMarkers:
        # deterministic markers; ensure sunrise < sunset < next_sunrise
        t0 = datetime(day.year, day.month, day.day, 7, 0, tzinfo=timezone.utc)
        return DayMarkers(
            sunrise=t0,
            solar_noon=t0 + timedelta(hours=5),
            sunset=t0 + timedelta(hours=10),
            next_sunrise=t0 + timedelta(days=1),
        )


class FakeMoon(MoonPhaseProvider):
    def get_phase_label(self, *, day: date, point: GeoPoint, tz: str) -> str:
        return "TestPhase"


def test_build_range_count_and_order_and_hours_shape() -> None:
    ctx = BuildContext(city="X", point=GeoPoint(lat=0.0, lon=0.0), tz="UTC")
    days = build_range(
        ctx=ctx,
        start=date(2026, 1, 1),
        end=date(2026, 1, 3),
        markers_provider=FakeMarkers(),
        moon_provider=FakeMoon(),
    )

    assert [d.day.isoformat() for d in days] == ["2026-01-01", "2026-01-02", "2026-01-03"]
    assert all(d.moon_phase == "TestPhase" for d in days)
    assert all(len(d.hours.day) == 12 for d in days)
    assert all(len(d.hours.night) == 12 for d in days)
    assert days[0].sun_sign == CAPRICORN
