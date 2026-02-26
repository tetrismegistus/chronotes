from __future__ import annotations

from datetime import date

import pytest

from chronotes.services.date_ranges import year_bounds, week_bounds


def test_year_bounds() -> None:
    start, end = year_bounds(2026)
    assert start == date(2026, 1, 1)
    assert end == date(2026, 12, 31)


def test_year_bounds_rejects_nonpositive() -> None:
    with pytest.raises(ValueError):
        year_bounds(0)


def test_week_bounds_monday_start() -> None:
    # 2026-02-25 is a Wednesday
    start, end = week_bounds(date(2026, 2, 25), week_start="mon")
    assert start == date(2026, 2, 23)
    assert end == date(2026, 3, 1)


def test_week_bounds_sunday_start() -> None:
    start, end = week_bounds(date(2026, 2, 25), week_start="sun")
    assert start == date(2026, 2, 22)
    assert end == date(2026, 2, 28)
