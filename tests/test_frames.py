import math

from satellite_tracker.calc.frames import WGS84_A, WGS84_E2, WGS84_F, geodetic_to_ecef


def test_equator_zero_altitude():
    # At the equator, altitude 0 coordinates should be (WGS84_A, 0, 0)
    lat_rad = 0.0
    lon_rad = 0.0
    alt_m = 0.0

    x, y, z = geodetic_to_ecef(lat_rad, lon_rad, alt_m)

    assert math.isclose(x, WGS84_A, rel_tol=1e-9)
    assert math.isclose(y, 0.0, abs_tol=1e-9)
    assert math.isclose(z, 0.0, abs_tol=1e-9)
