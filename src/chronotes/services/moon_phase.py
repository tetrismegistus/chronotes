from __future__ import annotations

from datetime import date, datetime, timezone


SYNODIC_MONTH_DAYS = 29.530588853  # mean synodic month length


# Widely-used reference new moon epoch for simple algorithms.
# We treat this as an internal constant; we don't test exact event dates.
_REF_NEW_MOON_UTC = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)


_PHASE_LABELS_8 = (
    "New",
    "Waxing Crescent",
    "First Quarter",
    "Waxing Gibbous",
    "Full",
    "Waning Gibbous",
    "Last Quarter",
    "Waning Crescent",
)


def _to_utc_noon(d: date) -> datetime:
    # Noon avoids edge cases around midnight boundaries.
    return datetime(d.year, d.month, d.day, 12, 0, tzinfo=timezone.utc)


def moon_phase_fraction(d: date) -> float:
    """
    Return lunar phase as a fraction in [0, 1), where:
      0.0   ~ New Moon
      0.25  ~ First Quarter
      0.5   ~ Full Moon
      0.75  ~ Last Quarter

    Pure approximation: no location, no downloads.
    """
    t = _to_utc_noon(d)
    days = (t - _REF_NEW_MOON_UTC).total_seconds() / 86400.0
    # modulo synodic month
    age = days % SYNODIC_MONTH_DAYS
    frac = age / SYNODIC_MONTH_DAYS
    # numeric stability
    if frac < 0:
        frac += 1.0
    if frac >= 1.0:
        frac -= 1.0
    return frac


def moon_phase_label(d: date) -> str:
    """
    Map phase fraction to 8 labels (nearest octant).
    """
    frac = moon_phase_fraction(d)
    idx = int((frac * 8.0) + 0.5) % 8
    return _PHASE_LABELS_8[idx]


def phase_label_index(label: str) -> int:
    """
    Helper for tests / tooling: stable label ordering 0..7.
    """
    return _PHASE_LABELS_8.index(label)
