from __future__ import annotations

from datetime import date

from chronotes.providers.astronomy_astral import AstralDayMarkersProvider
from chronotes.providers.contracts import GeoPoint


def test_astral_provider_returns_tzaware_and_increasing_markers() -> None:
    prov = AstralDayMarkersProvider()
    # Indianapolis-ish; values don’t matter, invariants do.
    point = GeoPoint(lat=39.7684, lon=-86.1581)
    tz = "America/Indiana/Indianapolis"
    d = date(2026, 1, 15)

    m = prov.get_markers(day=d, point=point, tz=tz)

    assert m.sunrise.tzinfo is not None
    assert m.solar_noon.tzinfo is not None
    assert m.sunset.tzinfo is not None
    assert m.next_sunrise.tzinfo is not None

    assert m.sunrise < m.solar_noon < m.sunset < m.next_sunrise
    assert m.next_sunrise.date() in {date(2026, 1, 16), date(2026, 1, 15)}  # DST edge safety
