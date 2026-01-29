from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Iterable

from chronotes.domain.models import DailyPageData
from chronotes.domain.planets import WEEKDAY_RULERS
from chronotes.providers.contracts import DayMarkersProvider, GeoPoint, MoonPhaseProvider
from chronotes.services.planetary_hours import build_planetary_hours
from chronotes.services.sun_sign import sun_sign_for_day

@dataclass(frozen=True, slots=True)
class BuildContext:
    city: str
    point: GeoPoint
    tz: str


def day_ruler_for(d: date):
    # Python: Monday=0..Sunday=6
    return WEEKDAY_RULERS[d.weekday()]


def iter_dates(start: date, end: date) -> Iterable[date]:
    if end < start:
        raise ValueError("Expected end >= start.")
    d = start
    while d <= end:
        yield d
        d = d + timedelta(days=1)


def build_daily_page_data(
    *,
    ctx: BuildContext,
    day: date,
    markers_provider: DayMarkersProvider,
    moon_provider: MoonPhaseProvider,
) -> DailyPageData:
    markers = markers_provider.get_markers(day=day, point=ctx.point, tz=ctx.tz)
    moon = moon_provider.get_phase_label(day=day, point=ctx.point, tz=ctx.tz)
    ruler = day_ruler_for(day)
    hours = build_planetary_hours(day_ruler=ruler, markers=markers)
    sun_sign = sun_sign_for_day(day)

    return DailyPageData(
        city=ctx.city,
        day=day,
        day_ruler=ruler,
        moon_phase=moon,
        markers=markers,
        hours=hours,
        sun_sign=sun_sign
    )


def build_range(
    *,
    ctx: BuildContext,
    start: date,
    end: date,
    markers_provider: DayMarkersProvider,
    moon_provider: MoonPhaseProvider,
) -> list[DailyPageData]:
    return [
        build_daily_page_data(
            ctx=ctx,
            day=d,
            markers_provider=markers_provider,
            moon_provider=moon_provider,
        )
        for d in iter_dates(start, end)
    ]
