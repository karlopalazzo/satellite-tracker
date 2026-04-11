class ConstellationTracker:
    """
    Tracks multiple satellites for a single observer.
    """

    def __init__(self, observer):
        self.observer = observer
        self.trackers = {}

    def add_satellite(self, name, satrec):
        from .tracker import SatelliteTracker

        self.trackers[name] = SatelliteTracker(satrec, self.observer)

    def add_satellite_from_norad(self, name: str, norad_id: int):
        from ..infrastructure.tle_provider import get_satellite_tle
        from ..calc.propagator import propagate_satellite

        line1, line2 = get_satellite_tle(norad_id)
        sat = propagate_satellite(line1, line2)

        self.add_satellite(name, sat)

    def get_all_positions(self, obs_time=None):
        results = {}

        for name, tracker in self.trackers.items():
            az, el, rng = tracker.get_az_el_range(obs_time)

            results[name] = {"azimuth": az, "elevation": el, "range": rng, "visible": el > 0}

        return results
