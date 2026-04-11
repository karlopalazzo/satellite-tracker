import pytest
import numpy as np
from datetime import datetime, timezone

from sgp4.api import Satrec

from satellite_tracker.domain.tracker import SatelliteTracker
from satellite_tracker.domain.observer import Observer


# example TLE ISS
line1 = "1 25544U 98067A   26064.12345678  .00001234  00000-0  12345-4 0  9991"
line2 = "2 25544  51.6441  21.0021 0004233 123.4567 246.7890 15.4891234567890"

@pytest.fixture(scope="module")
def tracker():
    satellite = Satrec.twoline2rv(line1, line2)

    # observer
    observer = Observer(
        latitude_deg=51.62773,
        longitude_deg=15.88198,
        altitude_m=126.0
    )

    return SatelliteTracker(satellite, observer)

obs_time = datetime(2026, 3, 5, 18, 30, 0, tzinfo=timezone.utc)


def test_tracker_returns_valid_values(tracker):
    az, el, rng = tracker.get_az_el_range(obs_time)

    # Assertions (just checking if values are within reasonable ranges)
    assert 0 <= az < 2 * np.pi, f"Azimuth out of range: {az}"
    assert -np.pi / 2 <= el <= np.pi / 2, f"Elevation out of range: {el}"
    assert rng > 300000, f"Range should be greater than 300000: {rng}"


def test_tracker_returns_accurate_values(tracker):
    new_obs_time = datetime(2026, 3, 5, 18, 35, 0, tzinfo=timezone.utc)
    az, el, rng = tracker.get_az_el_range(new_obs_time)
    expected_el_deg = -16.36  # Expected elevation in degrees
    assert abs(np.degrees(el) - expected_el_deg) < 0.5, f"Elevation differs: {np.degrees(el)} vs {expected_el_deg}"
    # NOTE: value depends on TLE epoch and model precision


def test_tracker_is_consistent_over_time(tracker):
    # Check that values are changing over time as expected
    obs_time2 = datetime(2026, 3, 5, 18, 40, 0, tzinfo=timezone.utc)
    az1, el1, rng1 = tracker.get_az_el_range(obs_time)
    az2, el2, rng2 = tracker.get_az_el_range(obs_time2)
    assert not np.isclose(az1, az2), f"Azimuth should change over time: {az1} vs {az2}"
    assert not np.isclose(el1, el2), f"Elevation should change over time: {el1} vs {el2}"
    assert not np.isclose(rng1, rng2), f"Range should change over time: {rng1} vs {rng2}"


def test_tracker_is_deterministic(tracker):
    az1, el1, rng1 = tracker.get_az_el_range(obs_time)
    az2, el2, rng2 = tracker.get_az_el_range(obs_time)

    assert np.isclose(az1, az2, atol=1e-1), f"Azimuth values differ: {az1} vs {az2}"
    assert np.isclose(el1, el2, atol=1e-1), f"Elevation values differ: {el1} vs {el2}"
    assert np.isclose(rng1, rng2, atol=1.0), f"Range values differ: {rng1} vs {rng2}"


def test_tracker_below_horizon(tracker):
    # Using a time when the satellite is expected to be below the horizon
    obs_time = datetime(2026, 3, 5, 3, 0, 0, tzinfo=timezone.utc)
    az, el, rng = tracker.get_az_el_range(obs_time)

    assert el < 0, f"Satellite should be below horizon (negative elevation), got: {el}"


def test_tracker_above_horizon(tracker):
    # Using a time when the satellite is expected to be above the horizon
    obs_time = datetime(2026, 4, 5, 10, 25, 0, tzinfo=timezone.utc)
    az, el, rng = tracker.get_az_el_range(obs_time)

    assert el > 0, f"Satellite should be above horizon (positive elevation), got: {el}"
