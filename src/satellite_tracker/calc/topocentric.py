import numpy as np


def ecef_to_enu(
    observer_ecef: np.ndarray,  # (3,) array shape
    satellite_ecef: np.ndarray,  # (3,) array shape
    lat_rad: float,
    lon_rad: float,
) -> np.ndarray:
    """
    Convert satellite position from ECEF to ENU coordinates relative to an observer.
    """
    # Vector from observer to satellite in ECEF
    delta_ecef = satellite_ecef - observer_ecef  # shape (3,)

    # rotation matrix ECEF -> ENU
    sin_lat = np.sin(lat_rad)
    cos_lat = np.cos(lat_rad)
    sin_lon = np.sin(lon_rad)
    cos_lon = np.cos(lon_rad)

    # shape (3, 3)
    R = np.array([
        [-sin_lon,              cos_lon,               0],
        [-sin_lat * cos_lon,   -sin_lat * sin_lon,   cos_lat],
        [cos_lat * cos_lon,    cos_lat * sin_lon,    sin_lat]
    ])

    # ENU coordinates by matrix multiplication
    enu = R @ delta_ecef  # shape (3,)
    return enu


def enu_to_az_el_range(enu: np.ndarray) -> tuple[float, float, float]:
    """
    Convert ENU coordinates to azimuth and elevation angles [rad] and range [m].
    """
    east, north, up = enu

    # range is sqrt (east^2 + north^2 + up^2)
    range_m = np.linalg.norm(enu)     # linalg.norm is more stable than sqrt(east**2 + north**2 + up**2)
    if range_m == 0:
        return 0.0, 0.0, 0.0          # avoid division by zero in el_rad and ensure valid input for arcsin
    # Note: linalg.norm will never be ngative, no need to check for negative range.

    # azimuth is atan2(east, north) - note the order for atan2
    az_rad = np.arctan2(east, north)  # range [-pi, pi]
    if az_rad < 0:
        az_rad += 2 * np.pi           # convert to range [0, 2*pi] for consistency with tracking conventions

    # elevation is arcsin(up / range), np.clip() ensures the input to arcsin is in the valid range [-1, 1] to avoid NaNs due to floating point errors.
    ratio = np.clip(up / range_m, -1.0, 1.0)
    el_rad = np.arcsin(ratio)         # range [-pi/2, pi/2]

    return az_rad, el_rad, range_m