import numpy as np
from math import degrees
from sgp4.api import Satrec
from datetime import datetime, timezone
from satellite_tracker.calc.frames import geodetic_to_ecef, gmst_from_jd, eci_to_ecef
from satellite_tracker.calc.propagator import propagate_to_eci
from satellite_tracker.calc.topocentric import ecef_to_enu, enu_to_az_el_range

def test_iss_position():
    # example TLE ISS
    line1 = "1 25544U 98067A   26064.12345678  .00001234  00000-0  12345-4 0  9991"
    line2 = "2 25544  51.6441  21.0021 0004233 123.4567 246.7890 15.4891234567890"
    satellite = Satrec.twoline2rv(line1, line2)

    # observer
    lat_rad = np.radians(51.62773)
    lon_rad = np.radians(15.88198)
    alt_m = 126.0

    # particular UTC
    obs_time = datetime(2026, 3, 5, 18, 30, 0, tzinfo=timezone.utc)

    r_eci, jd, fr = propagate_to_eci(satellite, obs_time)
    gmst_rad = gmst_from_jd(jd, fr)
    r_ecef = eci_to_ecef(r_eci, gmst_rad)
    observer_ecef = np.array(geodetic_to_ecef(lat_rad, lon_rad, alt_m))
    enu = ecef_to_enu(observer_ecef, r_ecef, lat_rad, lon_rad)
    az, el, rng = enu_to_az_el_range(enu)

    expected_el_deg = -27.29

    assert abs(degrees(el) - expected_el_deg) < 0.5, f"Elewacja różni się: {degrees(el)} vs {expected_el_deg}"