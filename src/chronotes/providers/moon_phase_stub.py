from __future__ import annotations

from datetime import date

from chronotes.providers.contracts import GeoPoint, MoonPhaseProvider


class StubMoonPhaseProvider(MoonPhaseProvider):
    def get_phase_label(self, *, day: date, point: GeoPoint, tz: str) -> str:
        return "Unknown"
