from sgp4.api import Satrec, jday
import numpy as np
import math

# WGS84 elipsoid constants
WGS84_A = 6378137.0  # Semi-major axis in meters
WGS84_F = 1 / 298.257223563  # Flattening
WGS84_E2 = 2 * WGS84_F - WGS84_F ** 2  # Square of eccentricity


def geodetic_to_ecef(
    lat_rad: float,
    lon_rad: float,
    alt_m: float
) -> tuple[float, float, float]:
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
    N = WGS84_A / math.sqrt(1 - WGS84_E2 * sin_lat ** 2)

    x = (N + alt_m) * cos_lat * cos_lon
    y = (N + alt_m) * cos_lat * sin_lon
    z = (N * (1 - WGS84_E2) + alt_m) * sin_lat

    return x, y, z


def satellite_tle_to_eci(satellite: Satrec, year, month, day, hour, minute, second) -> tuple[float, float, float]:
    """
    Convert satellite TLE data to ECI coordinates at a given time.
    """
    jd, fr = jday(year, month, day, hour, minute, second)  # Get Julian date and fraction
    e, r, v = satellite.sgp4(jd, fr)  # Get ECI position and velocity: error code, position (km), velocity (km/s)
    if e != 0:
        raise ValueError(f"SGP4 error code: {e}")
    return np.array(r), jd, fr  # r = [x, y, z] ECI in kilometers with jd and fr for GMST calculation


def gmst_from_jd(jd: float, fr: float) -> float:
    """
    Compute GMST in radians from Julian date and fraction.
    """
    # Formula from Vallado „Fundamentals of Astrodynamics and Applications”
    T = (jd - 2451545.0) / 36525.0  # Julian centuries since J2000.0
    # Linear growth of GMST in seconds, plus small corrections for T^2 and T^3 terms. The result is in seconds.
    gmst_sec = 67310.54841 + (876600 * 3600 + 8640184.812866) * T + 0.093104 * T ** 2 - 6.2e-6 * T ** 3
    gmst_sec = gmst_sec % 86400  # Wrap to [0, 86400) seconds
    gmst_rad = (gmst_sec / 86400) * 2 * math.pi  # Convert seconds to radians
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


def get_satellite_az_el_range(observer_lat_rad: float, observer_lon_rad: float, observer_alt_m: float, satellite: Satrec, obs_time: datetime = None) -> tuple[float, float, float]:
    """
    Get satellite azimuth [rad], elevation [rad] and range [m] from observer's geodetic coordinates and satellite TLE data.
    If obs_time is None, use current UTC time.
    
    Parameters:
        observer_lat_rad: Observer's latitude in radians
        observer_lon_rad: Observer's longitude in radians
        observer_alt_m: Observer's altitude in meters
        satellite: Satellite TLE record (Satrec object)
        obs_time: Observation time (datetime object) or None for current UTC time
    
    Returns:
        tuple[float, float, float]: azimuth [rad], elevation [rad], range [m]
    """
    # Pipeline 1: UTC time to be used as input for satellite TLE to ECI conversion
    if obs_time is None:
        obs_time = datetime.now(timezone.utc)
    
    year, month, day = obs_time.year, obs_time.month, obs_time.day
    hour, minute = obs_time.hour, obs_time.minute
    second = obs_time.second + obs_time.microsecond / 1e6

    # Pipeline 2: Satelite ECI and Julian Date using satellite TLE and Pipeline 1 time
    r_eci, jd, fr = satellite_tle_to_eci(satellite, year, month, day, hour, minute, second)

    # Pipeline 3: GMST using Pipeline 2 Julian Date and fraction
    gmst_rad = gmst_from_jd(jd, fr)

    # Pipeline 4: Satellite ECI -> ECEF using Pipeline 2 ECI and Pipeline 3 GMST
    r_ecef = eci_to_ecef(r_eci, gmst_rad) * 1000  # Convert km to m

    # Pipeline 5 Observer geodetic to ECEF
    observer_ecef = np.array(geodetic_to_ecef(observer_lat_rad, observer_lon_rad, observer_alt_m))

    # Pipeline 6: Satellite ECEF -> ENU using Pipeline 4 Satellite ECEF, Pipeline 5 Observer ECEF, and observer's geodetic coordinates
    enu = ecef_to_enu(observer_ecef, r_ecef, observer_lat_rad, observer_lon_rad)

    # Pipeline 7: Azimuth, elevation, range using ENU from Pipeline 6
    az_rad, el_rad, range_m = enu_to_az_el_range(enu)

    return az_rad, el_rad, range_m


