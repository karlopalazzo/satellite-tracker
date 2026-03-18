from .observer import Observer


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

    def get_all_positions(self, obs_time=None):
        results = {}

        for name, tracker in self.trackers.items():
            az, el, rng = tracker.get_az_el_range(obs_time)

            results[name] = {"azimuth": az, "elevation": el, "range": rng, "visible": el > 0}

        return results
