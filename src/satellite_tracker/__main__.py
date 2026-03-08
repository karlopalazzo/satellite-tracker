from datetime import datetime, timezone
from math import degrees
from .calc.propagator import propagate_satellite
from .infrastructure.tle_provider import get_satellite_tle
from .domain.observer import Observer
from .domain.tracker import SatelliteTracker

norad_id = 25544
line1, line2 = get_satellite_tle(norad_id)

satellite = propagate_satellite(line1, line2)

observer = Observer(
    latitude_deg=51.62773,
    longitude_deg=15.88198,
    altitude_m=126.0
)


tracker = SatelliteTracker(
    satellite,
    observer
)

# Pipeline:
# Satellite ECI → ECEF → Topocentric ENU → Azimuth/Elevation/Range
az, el, rng = tracker.get_az_el_range()

print(f"Azimuth: {degrees(az):.2f} deg, \
        Elevation: {degrees(el):.2f} deg, \
        Range: {rng:.2f} m")

if el > 0:
    print("Target over horizon.")
else:
    print("Target under horizon.")