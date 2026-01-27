from __future__ import annotations

from datetime import date

import pytest

from chronotes.services.date_ranges import year_bounds


def test_year_bounds() -> None:
    start, end = year_bounds(2026)
    assert start == date(2026, 1, 1)
    assert end == date(2026, 12, 31)


def test_year_bounds_rejects_nonpositive() -> None:
    with pytest.raises(ValueError):
        year_bounds(0)
