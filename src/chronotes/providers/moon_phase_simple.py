from __future__ import annotations

from datetime import date

from chronotes.providers.contracts import GeoPoint, MoonPhaseProvider
from chronotes.services.moon_phase import moon_phase_label


class SimpleMoonPhaseProvider(MoonPhaseProvider):
    def get_phase_label(self, *, day: date, point: GeoPoint, tz: str) -> str:
        # This implementation ignores point/tz (phase is global-ish for our purposes).
        return moon_phase_label(day)
