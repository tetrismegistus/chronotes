from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from astral import LocationInfo
from astral.sun import sun

from chronotes.domain.models import DayMarkers
from chronotes.providers.contracts import DayMarkersProvider, GeoPoint


class AstralDayMarkersProvider(DayMarkersProvider):
    def get_markers(self, *, day: date, point: GeoPoint, tz: str) -> DayMarkers:
        tzinfo = ZoneInfo(tz)

        # LocationInfo wants a name/region; we don't actually need them for solar calc.
        loc = LocationInfo(name="chronotes", region="", timezone=tz, latitude=point.lat, longitude=point.lon)
        s = sun(loc.observer, date=day, tzinfo=tzinfo)

        sunrise: datetime = s["sunrise"]
        sunset: datetime = s["sunset"]
        noon: datetime = s["noon"]

        # Next sunrise: compute for the next day.
        next_day = day + timedelta(days=1)
        s2 = sun(loc.observer, date=next_day, tzinfo=tzinfo)
        next_sunrise: datetime = s2["sunrise"]

        return DayMarkers(
            sunrise=sunrise,
            solar_noon=noon,
            sunset=sunset,
            next_sunrise=next_sunrise,
        )
