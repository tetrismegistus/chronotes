from __future__ import annotations

from datetime import date, timedelta
from typing import Literal


def year_bounds(year: int) -> tuple[date, date]:
    if year < 1:
        raise ValueError("year must be >= 1")
    return date(year, 1, 1), date(year, 12, 31)


def week_bounds(
    containing_day: date,
    *,
    week_start: Literal["mon", "sun"] = "mon",
) -> tuple[date, date]:
    """
    Return (start, end) inclusive for the week containing `containing_day`.

    - week_start="mon": ISO-style week (Mon..Sun)
    - week_start="sun": US-style week (Sun..Sat)
    """
    if week_start not in ("mon", "sun"):
        raise ValueError("week_start must be 'mon' or 'sun'")

    # Python: Monday=0 ... Sunday=6
    target = 0 if week_start == "mon" else 6
    delta = (containing_day.weekday() - target) % 7
    start = containing_day - timedelta(days=delta)
    end = start + timedelta(days=6)
    return start, end
