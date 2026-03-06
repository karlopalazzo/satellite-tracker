import numpy as np
from datetime import datetime, timezone

from satellite_tracker.calc.frames import (
    geodetic_to_ecef,
    gmst_from_jd,
    eci_to_ecef
)

from satellite_tracker.calc.topocentric import (
    ecef_to_enu,
    enu_to_az_el_range
)

from satellite_tracker.calc.propagator import propagate_to_eci


class SatelliteTracker:
    """
    High-level satellite tracking pipeline.
    Converts TLE propagation results into azimuth, elevation and range
    for a given observer's coordinates.
    """

    def __init__(self, satellite: Satrec, obs_lat_rad: float, obs_lon_rad: float, obs_alt_m: float):
        self.satellite = satellite
        self.obs_lat = obs_lat_rad
        self.obs_lon = obs_lon_rad
        self.obs_alt = obs_alt_m

        # Pre-computing observer ECEF
        self.obs_ecef = np.array(
            geodetic_to_ecef(obs_lat_rad, obs_lon_rad, obs_alt_m)
        )

    def get_az_el_range(self, obs_time: datetime | None = None):
        """
        Compute satellite azimuth, elevation and range for given time
        """
        if obs_time is None:
            obs_time = datetime.now(timezone.utc)
            
        r_eci, jd, fr = propagate_to_eci(self.satellite, obs_time)

        gmst_rad = gmst_from_jd(jd, fr)

        r_ecef = eci_to_ecef(r_eci, gmst_rad)

        enu = ecef_to_enu(
            self.obs_ecef,
            r_ecef,
            self.obs_lat,
            self.obs_lon
        )

        az_rad, el_rad, range_m = enu_to_az_el_range(enu)

        return az_rad, el_rad, range_m

    def is_visible(self, obs_time: datetime | None = None):
        """
        Check whether satellite is over horizon.
        """
        _, el_rad, _ = self.get_az_el_range(obs_time)
        return el_rad > 0