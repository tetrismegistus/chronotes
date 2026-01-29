from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from .planets import Planet


@dataclass(frozen=True, slots=True)
class DayMarkers:
    sunrise: datetime
    solar_noon: datetime
    sunset: datetime
    next_sunrise: datetime


@dataclass(frozen=True, slots=True)
class PlanetaryHour:
    ruler: Planet
    start: datetime
    end: datetime


@dataclass(frozen=True, slots=True)
class PlanetaryHours:
    day: tuple[PlanetaryHour, ...]   # 12
    night: tuple[PlanetaryHour, ...] # 12


@dataclass(frozen=True, slots=True)
class DailyPageData:
    city: str
    day: date
    day_ruler: Planet
    moon_phase: str
    markers: DayMarkers
    hours: PlanetaryHours


@dataclass(frozen=True, slots=True)
class SunSign:
    key: str 
    name: str
    unicode: str
    latex: str
