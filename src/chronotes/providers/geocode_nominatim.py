from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import json
import urllib.parse
import urllib.request

from .geocode_base import GeocodeProvider, GeocodeResult


@dataclass(frozen=True)
class NominatimGeocodeProvider(GeocodeProvider):
    user_agent: str
    endpoint: str = "https://nominatim.openstreetmap.org/search"
    timeout_s: float = 10.0

    def geocode(self, city: str) -> Optional[GeocodeResult]:
        q = city.strip()
        if not q:
            return None

        params = {
            "q": q,
            "format": "json",
            "limit": "1",
        }
        url = f"{self.endpoint}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})

        with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        if not data:
            return None

        hit = data[0]
        return GeocodeResult(
            display_name=hit.get("display_name", q),
            lat=float(hit["lat"]),
            lon=float(hit["lon"]),
        )
