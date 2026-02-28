from math import radians, degrees
from .frames import get_satellite_az_el
from sgp4.api import Satrec

# Observer's geodetic coordinates
observer_lat_rad = math.radians(52.2297)  # Warsaw latitude in radians
observer_lon_rad = math.radians(21.0122)  # Warsaw longitude in radians
observer_alt_m = 100.0  # Observer altitude in meters

# satrec: satellite TLE
satellite = Satrec.twoline2rv(line1, line2)  # Initialize satellite record from TLE lines

# Pipeline
# Satelite: r_eci:ECI -> r_ecef:ECEF -> observer_ecef:ECEF -> enu:ENU -> az_rad, el_rad, range_m
az_rad, el_rad, range_m = get_satellite_az_el(observer_lat_rad, observer_lon_rad, observer_alt_m, satellite)

print(f"Azimuth: {degrees(az_rad):.2f} deg, Elevation: {degrees(el_rad):.2f} deg, Range: {range_m:.2f} m")