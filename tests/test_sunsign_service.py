from dataclasses import FrozenInstanceError
from datetime import date

from chronotes.domain import sunsigns as ss
from chronotes.services.sun_sign import sun_sign_for_day


def test_sun_sign_for_day_returns_correct_sign():
    cases = [
        (date(2026, 3, 20), ss.PISCES),
        (date(2026, 3, 21), ss.ARIES),
        (date(2026, 4, 19), ss.ARIES),
        (date(2026, 4, 20), ss.TAURUS),
        (date(2026, 12, 21), ss.SAGITTARIUS),
        (date(2026, 12, 22), ss.CAPRICORN),
        (date(2026, 1, 19), ss.CAPRICORN),
        (date(2026, 1, 20), ss.AQUARIUS),
        (date(1999, 3, 21), ss.ARIES),
    ]
    
    for c in cases:
        result = sun_sign_for_day(c[0])
        expected = c[1]
        assert result == expected
