from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Planet:
    """
    Domain model for a classical planet / luminary used in planetary hours.

    Notes:
    - Keep this pure data. No datetime, no IO, no LaTeX assumptions.
    - `key` is the stable programmatic identifier.
    """
    key: str
    name: str
    unicode: str
    bg: str | None = None
    fg: str | None = None


# Canonical planet instances (matching the legacy project data)
MOON = Planet(key="moon", name="Moon", unicode="\u263D", bg="violet", fg="white")
MARS = Planet(key="mars", name="Mars", unicode="\u2642", bg="red", fg="white")
MERCURY = Planet(key="mercury", name="Mercury", unicode="\u263F", bg="orange", fg="white")
JUPITER = Planet(key="jupiter", name="Jupiter", unicode="\u2643", bg="blue", fg="white")
VENUS = Planet(key="venus", name="Venus", unicode="\u2640", bg="green", fg="white")
SATURN = Planet(key="saturn", name="Saturn", unicode="\u2644", bg="black", fg="white")
SUN = Planet(key="sun", name="Sun", unicode="\u2609", bg="yellow", fg="white")


# Ordering used for planetary hours (Chaldean order)
CHALDEAN_ORDER: tuple[Planet, ...] = (
    SATURN,
    JUPITER,
    MARS,
    SUN,
    VENUS,
    MERCURY,
    MOON,
)

# Day rulers by weekday index *as used in the legacy code*.
# (Interpretation of weekday index belongs in services.)
WEEKDAY_RULERS: tuple[Planet, ...] = (
    MOON,
    MARS,
    MERCURY,
    JUPITER,
    VENUS,
    SATURN,
    SUN,
)

BY_KEY: dict[str, Planet] = {p.key: p for p in (MOON, MARS, MERCURY, JUPITER, VENUS, SATURN, SUN)}
BY_NAME: dict[str, Planet] = {p.name: p for p in (MOON, MARS, MERCURY, JUPITER, VENUS, SATURN, SUN)}
