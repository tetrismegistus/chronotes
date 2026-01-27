from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from chronotes.domain.models import DayMarkers


@dataclass(frozen=True, slots=True)
class GeoPoint:
    lat: float
    lon: float


class DayMarkersProvider:
    def get_markers(self, *, day: date, point: GeoPoint, tz: str) -> DayMarkers:
        raise NotImplementedError


class MoonPhaseProvider:
    def get_phase_label(self, *, day: date, point: GeoPoint, tz: str) -> str:
        raise NotImplementedError
