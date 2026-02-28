import numpy as np
import pytest
from iss_tracker.calc.topocentric import ecef_to_enu, enu_to_az_el_range


def test_ecef_to_enu_east_direction():
    # Operating in ecef, observer in prime meridian, equator, under ground, satellite 1000m east.
    # Note: not realistic, just abstract geometric case.
    obs_ecef = np.array([1113194.907, 0.0, 0.0])
    sat_ecef = np.array([1113194.907, 1000.0, 0.0])

    lat_rad = np.radians(0.0)  # 0° latitude
    lon_rad = np.radians(0.0)  # 0° longitude

    enu = ecef_to_enu(obs_ecef, sat_ecef, lat_rad, lon_rad)

    expected_enu = np.array([1000.0, 0.0, 0.0])  # Expecting 1000m east, 0 north, 0 up

    assert np.allclose(enu, expected_enu, atol=1e-6), f"Expected ENU {expected_enu}, got {enu}"


@pytest.mark.parametrize(
    "enu, expected_az_deg, expected_el_deg, expected_range",
    [
        pytest.param(np.array([0.0, 0.0, 1000.0]), None, 90.0, 1000.0, id="up_1000m"),
        pytest.param(np.array([1000.0, 0.0, 0.0]), 90.0, 0.0, 1000.0, id="east_1000m"),
        pytest.param(np.array([0.0, 1000.0, 0.0]), 0.0, 0.0, 1000.0, id="north_1000m"),
        pytest.param(np.array([0.0, -1000.0, 0.0]), 180.0, 0.0, 1000.0, id="south_1000m"),
        pytest.param(np.array([0.0, 0.0, 0.0]), 0.0, 0.0, 0.0, id="zero_vector"),
    ]
)
def test_enu_to_az_el_range(enu, expected_az_deg, expected_el_deg, expected_range):
    az_rad, el_rad, range_m = enu_to_az_el_range(enu)

    if expected_az_deg is not None:
        assert np.isclose(az_rad, np.radians(expected_az_deg), atol=1e-6), f"Expected azimuth {expected_az_deg}°, got {np.degrees(az_rad)}°"
    
    assert np.isclose(el_rad, np.radians(expected_el_deg), atol=1e-6), f"Expected elevation {expected_el_deg}°, got {np.degrees(el_rad)}°"
    assert np.isclose(range_m, expected_range, atol=1e-6), f"Expected range {expected_range}m, got {range_m}m"
