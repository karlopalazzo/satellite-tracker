from datetime import datetime, timezone
from math import radians, degrees
from .calc.frames import get_satellite_az_el_range
from .calc.propagator import propagate_satellite
from .infrastructure.tle_provider import get_satellite_tle

# Observer's geodetic coordinates
observer_lat_rad = radians(51.62773)  # Wroclaw latitude in radians
observer_lon_rad = radians(15.88198)  # Wroclaw longitude in radians
observer_alt_m = 126.0  # Observer altitude in meters

# satrec: satellite TLE
line1, line2 = get_satellite_tle(25544)
print(line1, line2, sep='\n')
satellite = propagate_satellite(line1, line2)  # Initialize satellite record from TLE lines


# Satelite: r_eci:ECI -> r_ecef:ECEF -> observer_ecef:ECEF -> enu:ENU -> az_rad, el_rad, range_m
az_rad, el_rad, range_m = get_satellite_az_el_range(
    observer_lat_rad,
    observer_lon_rad,
    observer_alt_m,
    satellite,
    )

print(f"Azimuth: {degrees(az_rad):.2f} deg, \
        Elevation: {degrees(el_rad):.2f} deg, \
        Range: {range_m:.2f} m")

if degrees(el_rad) < 0:
    print("Target under horizon.")
else:
    print("Target over horizon.")