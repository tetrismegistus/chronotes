from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Optional


@dataclass(frozen=True)
class GeocodeResult:
    """A single geocoding match."""
    display_name: str
    lat: float
    lon: float


class GeocodeProvider(Protocol):
    def geocode(self, city: str) -> Optional[GeocodeResult]:
        """Return best match for a city string, or None if not found."""
        ...
