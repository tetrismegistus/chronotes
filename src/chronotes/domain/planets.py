from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Planet:
    key: str
    name: str
    unicode: str
    latex: str
    bg: str | None = None
    fg: str | None = None

MOON = Planet(key="moon", name="Moon", unicode="\u263D", latex=r"\leftmoon", bg="violet", fg="white")
MARS = Planet(key="mars", name="Mars", unicode="\u2642", latex=r"\mars", bg="red", fg="white")
MERCURY = Planet(key="mercury", name="Mercury", unicode="\u263F", latex=r"\mercury", bg="orange", fg="white")
JUPITER = Planet(key="jupiter", name="Jupiter", unicode="\u2643", latex=r"\jupiter", bg="blue", fg="white")
VENUS = Planet(key="venus", name="Venus", unicode="\u2640", latex=r"\venus", bg="green", fg="white")
SATURN = Planet(key="saturn", name="Saturn", unicode="\u2644", latex=r"\saturn", bg="black", fg="white")
SUN = Planet(key="sun", name="Sun", unicode="\u2609", latex=r"\astrosun", bg="yellow", fg="white")


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
