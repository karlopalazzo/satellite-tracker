import pytest
import math
from iss_tracker.domain.observer import Observer, ObserverValidationError


def test_observer_valid():
    obs = Observer(latitude_deg=45.0, longitude_deg=90.0, altitude_m=100.0)

    assert obs.latitude_deg == 45.0
    assert obs.longitude_deg == 90.0
    assert obs.altitude_m == 100.0

    # Check deg-to-rad conversion
    assert math.isclose(obs.latitude_rad, math.radians(45.0))
    assert math.isclose(obs.longitude_rad, math.radians(90.0))


def test_observer_invalid_latitude():
    with pytest.raises(ObserverValidationError):
        Observer(latitude_deg=100.0, longitude_deg=0.0, altitude_m=0.0)

    with pytest.raises(ObserverValidationError):
        Observer(latitude_deg=-100.0, longitude_deg=0.0, altitude_m=0.0)


def test_observer_invalid_longitude():
    with pytest.raises(ObserverValidationError):
        Observer(latitude_deg=0.0, longitude_deg=200.0, altitude_m=0.0)
    
    with pytest.raises(ObserverValidationError):
        Observer(latitude_deg=0.0, longitude_deg=-200.0, altitude_m=0.0)


def test_observer_invalid_altitude():
    with pytest.raises(ObserverValidationError):
        Observer(latitude_deg=0.0, longitude_deg=0.0, altitude_m=-2000.0)
    
    with pytest.raises(ObserverValidationError):
        Observer(latitude_deg=0.0, longitude_deg=0.0, altitude_m=200_000.0)