from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LocationConfig:
    city: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    tz: Optional[str] = None  # allow override, but CLI likely supplies


@dataclass(frozen=True)
class GeocodeConfig:
    provider: Optional[str] = None  # "nominatim" or None
    user_agent: Optional[str] = None


@dataclass(frozen=True)
class ChronotesConfig:
    location: LocationConfig = LocationConfig()
    geocode: GeocodeConfig = GeocodeConfig()


def merge_config(
    *,
    base: ChronotesConfig,
    override: ChronotesConfig,
) -> ChronotesConfig:
    """Shallow merge with 'override wins' semantics."""
    b = base.location
    o = override.location
    return ChronotesConfig(
        location=LocationConfig(
            city=o.city if o.city is not None else b.city,
            lat=o.lat if o.lat is not None else b.lat,
            lon=o.lon if o.lon is not None else b.lon,
            tz=o.tz if o.tz is not None else b.tz,
        )
    )
