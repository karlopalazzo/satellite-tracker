import numpy as np
from datetime import datetime, timezone
from sgp4.api import Satrec
from .observer import Observer

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

    def __init__(self, satellite: Satrec, observer: Observer):
        self.satellite = satellite
        self.observer = observer

        # Pre-computing observer ECEF
        self.obs_ecef = np.array(
            geodetic_to_ecef(
                self.observer.latitude_rad,
                self.observer.longitude_rad,
                self.observer.altitude_m
            )
        )

    def get_az_el_range(self, obs_time: datetime | None = None):
        """
        Compute satellite azimuth, elevation and range for a given time.
        """
        obs_time = self._resolve_time(obs_time)
            
        r_eci, jd, fr = propagate_to_eci(self.satellite, obs_time)

        gmst_rad = gmst_from_jd(jd, fr)

        r_ecef = eci_to_ecef(r_eci, gmst_rad)

        enu = ecef_to_enu(
            self.obs_ecef,
            r_ecef,
            self.observer.latitude_rad,
            self.observer.longitude_rad
        )

        az_rad, el_rad, range_m = enu_to_az_el_range(enu)

        return az_rad, el_rad, range_m

    def _resolve_time(self, obs_time: datetime | None) -> datetime:
        if obs_time is None:
            return datetime.now(timezone.utc)
        return obs_time