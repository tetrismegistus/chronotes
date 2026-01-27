from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from chronotes.domain.models import DayMarkers
from chronotes.domain.planets import CHALDEAN_ORDER, SUN, MOON, MARS
from chronotes.services.planetary_hours import build_planetary_hours


def _idx(order, planet):
    return [p.key for p in order].index(planet.key)


def test_build_planetary_hours_returns_12_and_tiles_intervals():
    # Deliberately choose intervals not divisible by 12 to force fractional handling.
    sunrise = datetime(2026, 1, 27, 7, 13, tzinfo=timezone.utc)
    sunset = datetime(2026, 1, 27, 17, 49, tzinfo=timezone.utc)
    next_sunrise = datetime(2026, 1, 28, 7, 11, tzinfo=timezone.utc)

    markers = DayMarkers(
        sunrise=sunrise,
        solar_noon=datetime(2026, 1, 27, 12, 31, tzinfo=timezone.utc),
        sunset=sunset,
        next_sunrise=next_sunrise,
    )

    hours = build_planetary_hours(day_ruler=SUN, markers=markers)

    assert len(hours.day) == 12
    assert len(hours.night) == 12

    # Day tiles sunrise -> sunset
    assert hours.day[0].start == sunrise
    assert abs((hours.day[-1].end - sunset).total_seconds()) < 1e-6
    for i in range(11):
        assert hours.day[i].end == hours.day[i + 1].start

    # Night tiles sunset -> next sunrise
    assert hours.night[0].start == sunset
    assert abs((hours.night[-1].end - next_sunrise).total_seconds()) < 1e-6
    for i in range(11):
        assert hours.night[i].end == hours.night[i + 1].start


def test_day_ruler_starts_day_table_and_progresses_in_chaldean_order():
    sunrise = datetime(2026, 1, 27, 6, 0, tzinfo=timezone.utc)
    sunset = datetime(2026, 1, 27, 18, 0, tzinfo=timezone.utc)
    next_sunrise = datetime(2026, 1, 28, 6, 0, tzinfo=timezone.utc)

    markers = DayMarkers(
        sunrise=sunrise,
        solar_noon=datetime(2026, 1, 27, 12, 0, tzinfo=timezone.utc),
        sunset=sunset,
        next_sunrise=next_sunrise,
    )

    hours = build_planetary_hours(day_ruler=MOON, markers=markers)

    # Day[0] ruler is the day ruler
    assert hours.day[0].ruler.key == MOON.key

    # Progression uses CHALDEAN_ORDER cycling
    start_idx = _idx(CHALDEAN_ORDER, MOON)
    expected = [CHALDEAN_ORDER[(start_idx + i) % 7].key for i in range(12)]
    got = [h.ruler.key for h in hours.day]
    assert got == expected


def test_night_table_starts_after_last_day_ruler_in_cycle():
    sunrise = datetime(2026, 1, 27, 6, 0, tzinfo=timezone.utc)
    sunset = datetime(2026, 1, 27, 18, 0, tzinfo=timezone.utc)
    next_sunrise = datetime(2026, 1, 28, 6, 0, tzinfo=timezone.utc)

    markers = DayMarkers(
        sunrise=sunrise,
        solar_noon=datetime(2026, 1, 27, 12, 0, tzinfo=timezone.utc),
        sunset=sunset,
        next_sunrise=next_sunrise,
    )

    hours = build_planetary_hours(day_ruler=MARS, markers=markers)

    last_day_ruler = hours.day[-1].ruler
    last_idx = _idx(CHALDEAN_ORDER, last_day_ruler)
    expected_first_night = CHALDEAN_ORDER[(last_idx + 1) % 7]

    assert hours.night[0].ruler.key == expected_first_night.key

    # And it should keep progressing in the same cycle
    start_idx = _idx(CHALDEAN_ORDER, expected_first_night)
    expected_night = [CHALDEAN_ORDER[(start_idx + i) % 7].key for i in range(12)]
    got_night = [h.ruler.key for h in hours.night]
    assert got_night == expected_night


def test_rejects_markers_with_non_increasing_boundaries():
    sunrise = datetime(2026, 1, 27, 7, 0, tzinfo=timezone.utc)
    sunset = datetime(2026, 1, 27, 6, 0, tzinfo=timezone.utc)  # invalid: before sunrise
    next_sunrise = datetime(2026, 1, 28, 7, 0, tzinfo=timezone.utc)

    markers = DayMarkers(
        sunrise=sunrise,
        solar_noon=datetime(2026, 1, 27, 12, 0, tzinfo=timezone.utc),
        sunset=sunset,
        next_sunrise=next_sunrise,
    )

    with pytest.raises(ValueError):
        build_planetary_hours(day_ruler=SUN, markers=markers)
