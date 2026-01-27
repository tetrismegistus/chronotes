from __future__ import annotations

from datetime import date


def year_bounds(year: int) -> tuple[date, date]:
    if year < 1:
        raise ValueError("year must be >= 1")
    return date(year, 1, 1), date(year, 12, 31)
