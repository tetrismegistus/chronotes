from __future__ import annotations

from datetime import date

from chronotes.providers.astronomy_astral import AstralDayMarkersProvider
from chronotes.providers.contracts import GeoPoint


def test_astral_daylight_duration_is_reasonable_winter_and_summer() -> None:
    prov = AstralDayMarkersProvider()
    point = GeoPoint(lat=39.7684, lon=-86.1581)  # Indianapolis-ish
    tz = "America/Indiana/Indianapolis"

    # Representative winter and summer dates
    for d in (date(2026, 1, 15), date(2026, 6, 15)):
        m = prov.get_markers(day=d, point=point, tz=tz)

        daylight_seconds = (m.sunset - m.sunrise).total_seconds()

        # Invariants, not astronomy correctness:
        assert daylight_seconds > 0
        assert daylight_seconds < 24 * 60 * 60
