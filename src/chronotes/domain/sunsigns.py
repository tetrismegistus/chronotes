from __future__ import annotations

from .models import SunSign

ARIES       = SunSign(key="aries",       name="Aries",       unicode="\u2648", latex=r"\aries")
TAURUS      = SunSign(key="taurus",      name="Taurus",      unicode="\u2649", latex=r"\taurus")
GEMINI      = SunSign(key="gemini",      name="Gemini",      unicode="\u264A", latex=r"\gemini")
CANCER      = SunSign(key="cancer",      name="Cancer",      unicode="\u264B", latex=r"\cancer")
LEO         = SunSign(key="leo",         name="Leo",         unicode="\u264C", latex=r"\leo")
VIRGO       = SunSign(key="virgo",       name="Virgo",       unicode="\u264D", latex=r"\virgo")
LIBRA       = SunSign(key="libra",       name="Libra",       unicode="\u264E", latex=r"\libra")
SCORPIO     = SunSign(key="scorpio",     name="Scorpio",     unicode="\u264F", latex=r"\scorpio")
SAGITTARIUS = SunSign(key="sagittarius", name="Sagittarius", unicode="\u2650", latex=r"\sagittarius")
CAPRICORN   = SunSign(key="capricorn",   name="Capricorn",   unicode="\u2651", latex=r"\capricornus")
AQUARIUS    = SunSign(key="aquarius",    name="Aquarius",    unicode="\u2652", latex=r"\aquarius")
PISCES      = SunSign(key="pisces",      name="Pisces",      unicode="\u2653", latex=r"\pisces")

SUN_SIGN_BOUNDARIES = (
    (1, 20, AQUARIUS),
    (2, 19, PISCES),
    (3, 21, ARIES),
    (4, 20, TAURUS),
    (5, 21, GEMINI),
    (6, 21, CANCER),
    (7, 23, LEO),
    (8, 23, VIRGO),
    (9, 23, LIBRA),
    (10, 23, SCORPIO),
    (11, 22, SAGITTARIUS),
    (12, 22, CAPRICORN),
)
