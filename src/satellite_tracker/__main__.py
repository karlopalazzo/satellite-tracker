from datetime import datetime, timezone
from math import degrees

from .calc.propagator import propagate_satellite
from .domain.constellation_tracker import ConstellationTracker
from .domain.observer import Observer
from .infrastructure.tle_provider import get_satellite_tle

observer = Observer(latitude_deg=51.62773, longitude_deg=15.88198, altitude_m=126.0)

constellation = ConstellationTracker(observer)

# ISS
line1, line2 = get_satellite_tle(25544)
iss = propagate_satellite(line1, line2)
constellation.add_satellite("ISS", iss)

# Hubble
line1, line2 = get_satellite_tle(20580)
hubble = propagate_satellite(line1, line2)
constellation.add_satellite("Hubble", hubble)

positions = constellation.get_all_positions()

for name, data in positions.items():
    print(name)

    print(
        f"Az: {degrees(data['azimuth']):.2f}° "
        f"El: {degrees(data['elevation']):.2f}° "
        f"Range: {data['range']:.0f} m"
    )

    if data["visible"]:
        print("Visible\n")
    else:
        print("Below horizon\n")
