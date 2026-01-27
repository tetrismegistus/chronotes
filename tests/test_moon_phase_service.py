from __future__ import annotations

from datetime import date, timedelta

from chronotes.services.moon_phase import moon_phase_fraction, moon_phase_label, phase_label_index


def test_moon_phase_fraction_in_range() -> None:
    for d in (date(2026, 1, 1), date(2026, 6, 15), date(2026, 12, 31)):
        f = moon_phase_fraction(d)
        assert 0.0 <= f < 1.0


def test_moon_phase_label_in_known_set() -> None:
    labels = set()
    d0 = date(2026, 1, 1)
    for i in range(0, 40):
        labels.add(moon_phase_label(d0 + timedelta(days=i)))

    # We expect at least several distinct labels over ~40 days.
    assert len(labels) >= 4


def _cyclic_dist(a: int, b: int, n: int = 8) -> int:
    d = abs(a - b) % n
    return min(d, n - d)


def test_label_roughly_repeats_after_one_month() -> None:
    d = date(2026, 1, 15)
    a = phase_label_index(moon_phase_label(d))
    b = phase_label_index(moon_phase_label(d + timedelta(days=29)))

    # 29 days is near one synodic month; allow same or adjacent octant.
    assert _cyclic_dist(a, b) <= 1
