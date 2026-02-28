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