import pytest
from dataclasses import FrozenInstanceError

from chronotes.domain.planets import (
    BY_KEY,
    CHALDEAN_ORDER,
    WEEKDAY_RULERS,
    Planet,
)


def test_planet_model_is_frozen():
    p = BY_KEY["moon"]
    with pytest.raises(FrozenInstanceError):
        p.name = "NotMoon"


def test_keys_unique_and_complete():
    keys = list(BY_KEY.keys())
    assert len(keys) == 7
    assert len(set(keys)) == 7
    assert set(keys) == {"moon", "mars", "mercury", "jupiter", "venus", "saturn", "sun"}


def test_chaldean_order_matches_legacy():
    assert [p.key for p in CHALDEAN_ORDER] == [
        "saturn",
        "jupiter",
        "mars",
        "sun",
        "venus",
        "mercury",
        "moon",
    ]


def test_weekday_rulers_matches_legacy_sequence():
    assert [p.key for p in WEEKDAY_RULERS] == [
        "moon",
        "mars",
        "mercury",
        "jupiter",
        "venus",
        "saturn",
        "sun",
    ]


def test_weekday_rulers_are_planets_and_unique():
    assert all(isinstance(p, Planet) for p in WEEKDAY_RULERS)
    assert len(WEEKDAY_RULERS) == 7
    assert len({p.key for p in WEEKDAY_RULERS}) == 7
