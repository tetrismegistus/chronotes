from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from chronotes.providers.contracts import GeoPoint
from chronotes.providers.geocode_base import GeocodeProvider


@dataclass(frozen=True, slots=True)
class ResolvedLocation:
    city_label: str
    point: GeoPoint


def resolve_location(
    *,
    city: Optional[str],
    lat: Optional[float],
    lon: Optional[float],
    geocoder: Optional[GeocodeProvider],
) -> ResolvedLocation:
    city = (city or "").strip()

    has_lat = lat is not None
    has_lon = lon is not None

    if has_lat ^ has_lon:
        raise ValueError("Provide both --lat and --lon, or neither.")

    # Explicit coordinates win.
    if has_lat and has_lon:
        label = city if city else f"{lat:.4f}, {lon:.4f}"
        return ResolvedLocation(city_label=label, point=GeoPoint(lat=float(lat), lon=float(lon)))

    # No coordinates -> require city + geocoder
    if not city:
        raise ValueError("Provide --city (for geocoding) or --lat/--lon (explicit coordinates).")

    if geocoder is None:
        raise ValueError("Geocoding is not configured. Provide --lat/--lon or configure a geocode provider.")

    hit = geocoder.geocode(city)
    if hit is None:
        raise ValueError(f"Could not geocode city: {city!r}")

    return ResolvedLocation(
        city_label=hit.display_name or city,
        point=GeoPoint(lat=float(hit.lat), lon=float(hit.lon)),
    )
