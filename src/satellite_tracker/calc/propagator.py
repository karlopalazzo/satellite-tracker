from datetime import datetime

import numpy as np
from sgp4.api import Satrec, jday


def propagate_satellite(line1: str, line2: str) -> Satrec:
    """Create Satrec object based on TLE lines."""
    return Satrec.twoline2rv(line1, line2)


def propagate_to_eci(satellite: Satrec, time: datetime):
    """
    Propagate satellite orbit to current time
    and return ECI position vector (meters).
    """

    jd, fr = jday(time.year, time.month, time.day, time.hour, time.minute, time.second + time.microsecond * 1e-6)
    e, r, v = satellite.sgp4(jd, fr)  # Get ECI position and velocity: error code, position (km), velocity (km/s)

    if e != 0:
        raise ValueError(f"SGP4 error code: {e}")

    r_eci_m = np.array(r) * 1000

    return r_eci_m, jd, fr
