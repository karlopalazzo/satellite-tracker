from math import degrees

from .domain.constellation_tracker import ConstellationTracker
from .domain.observer import Observer

observer = Observer(latitude_deg=51.62773, longitude_deg=15.88198, altitude_m=126.0)

constellation = ConstellationTracker(observer)

# ISS
constellation.add_satellite_from_norad("ISS", 25544)
# Hubble
constellation.add_satellite_from_norad("Hubble", 20580)

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
