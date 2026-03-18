import math
from datetime import datetime, timezone

import numpy as np
from sgp4.api import Satrec, jday
from sgp4.propagation import gstime

from .propagator import propagate_to_eci
from .topocentric import ecef_to_enu, enu_to_az_el_range

# WGS84 elipsoid constants
WGS84_A = 6378137.0  # Semi-major axis in meters
WGS84_F = 1 / 298.257223563  # Flattening
WGS84_E2 = 2 * WGS84_F - WGS84_F**2  # Square of eccentricity


def geodetic_to_ecef(lat_rad: float, lon_rad: float, alt_m: float) -> tuple[float, float, float]:
    """
    Convert geodetic coordinates (lat, lon, alt) to ECEF.
    All angles in radians, altitude in meters.
    Returns (x, y, z) in meters.
    """

    sin_lat = math.sin(lat_rad)
    cos_lat = math.cos(lat_rad)
    sin_lon = math.sin(lon_rad)
    cos_lon = math.cos(lon_rad)

    # Radius of curvature in the prime vertical
    N = WGS84_A / math.sqrt(1 - WGS84_E2 * sin_lat**2)

    x = (N + alt_m) * cos_lat * cos_lon
    y = (N + alt_m) * cos_lat * sin_lon
    z = (N * (1 - WGS84_E2) + alt_m) * sin_lat

    return x, y, z


def gmst_from_jd(jd: float, fr: float) -> float:
    """
    Compute GMST in radians from Julian date and fraction.
    """
    jd_full = jd + fr
    gmst_rad = gstime(jd_full)
    return gmst_rad


def eci_to_ecef(r_eci: np.ndarray, gmst_rad: float) -> np.ndarray:
    """
    Convert ECI coordinates to ECEF coordinates using the GMST angle.
    """
    x, y, z = r_eci
    cos_gmst = np.cos(gmst_rad)
    sin_gmst = np.sin(gmst_rad)
    x_ecef = cos_gmst * x + sin_gmst * y
    y_ecef = -sin_gmst * x + cos_gmst * y
    z_ecef = z
    return np.array([x_ecef, y_ecef, z_ecef])
