from __future__ import annotations

from datetime import timedelta
from typing import Sequence

from chronotes.domain.models import DayMarkers, PlanetaryHour, PlanetaryHours
from chronotes.domain.planets import CHALDEAN_ORDER, Planet


def _hour_length(start, end) -> timedelta:
    """
    Legacy behavior: floor to whole seconds after dividing by 12.
    """
    seconds = (end - start).total_seconds()
    if seconds <= 0:
        raise ValueError("Non-positive interval for planetary hours.")
    return timedelta(seconds=int(seconds // 12))


def _index_in_cycle(order: Sequence[Planet], planet: Planet) -> int:
    for i, p in enumerate(order):
        if p.key == planet.key:
            return i
    raise ValueError(f"Planet {planet.key!r} not found in hour_order cycle.")


def _build_table(
    *,
    start,
    end,
    start_ruler: Planet,
    hour_order: Sequence[Planet],
) -> tuple[PlanetaryHour, ...]:
    hour_len = _hour_length(start, end)
    idx = _index_in_cycle(hour_order, start_ruler)

    rows: list[PlanetaryHour] = []
    t = start
    for i in range(12):
        ruler = hour_order[(idx + i) % len(hour_order)]
        t2 = t + hour_len
        rows.append(PlanetaryHour(ruler=ruler, start=t, end=t2))
        t = t2

    # Ensure we exactly tile to `end` (legacy floored seconds will drift).
    # We force the last end to match the boundary to satisfy render expectations and tests.
    rows[-1] = PlanetaryHour(ruler=rows[-1].ruler, start=rows[-1].start, end=end)

    return tuple(rows)


def build_planetary_hours(
    *,
    day_ruler: Planet,
    markers: DayMarkers,
    hour_order: Sequence[Planet] = CHALDEAN_ORDER,
) -> PlanetaryHours:
    sunrise = markers.sunrise
    sunset = markers.sunset
    next_sunrise = markers.next_sunrise

    if not (sunrise < sunset < next_sunrise):
        raise ValueError("Expected sunrise < sunset < next_sunrise.")

    day = _build_table(
        start=sunrise,
        end=sunset,
        start_ruler=day_ruler,
        hour_order=hour_order,
    )

    # Night starts with the planet *after* the last day ruler in the same cycle
    last_day_ruler = day[-1].ruler
    last_idx = _index_in_cycle(hour_order, last_day_ruler)
    night_start_ruler = hour_order[(last_idx + 1) % len(hour_order)]

    night = _build_table(
        start=sunset,
        end=next_sunrise,
        start_ruler=night_start_ruler,
        hour_order=hour_order,
    )

    return PlanetaryHours(day=day, night=night)
