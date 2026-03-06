from datetime import datetime, timezone
from math import radians, degrees
from sgp4.api import Satrec
from .infrastructure.tle_provider import get_satellite_tle
from .domain.tracker import SatelliteTracker

norad_id = 25544
line1, line2 = get_satellite_tle(norad_id)

satellite = Satrec.twoline2rv(line1, line2)

# Observer's geodetic coordinates
observer_lat = radians(51.62773)  # Wroclaw latitude in radians
observer_lon = radians(15.88198)  # Wroclaw longitude in radians
observer_alt = 126.0  # Observer altitude in meters

tracker = SatelliteTracker(
    satellite,
    observer_lat,
    observer_lon,
    observer_alt
)

# Satelite: r_eci:ECI -> r_ecef:ECEF -> observer_ecef:ECEF -> enu:ENU -> az_rad, el_rad, range_m
az, el, rng = tracker.get_az_el_range()

print(f"Azimuth: {degrees(az):.2f} deg, \
        Elevation: {degrees(el):.2f} deg, \
        Range: {rng:.2f} m")

if tracker.is_visible():
    print("Target under horizon.")
else:
    print("Target over horizon.")