from chronotes.domain.models import SunSign
from chronotes.domain.sunsigns import CAPRICORN
from chronotes.domain.sunsigns import SUN_SIGN_BOUNDARIES

from datetime import date

def sun_sign_for_day(d: date) -> SunSign: 
   month = d.month
   day = d.day
   last_matching_sun_sign = CAPRICORN
   for boundary in SUN_SIGN_BOUNDARIES:
     if (month, day) >= (boundary[0], boundary[1]):
        last_matching_sun_sign = boundary[2]
   return last_matching_sun_sign

