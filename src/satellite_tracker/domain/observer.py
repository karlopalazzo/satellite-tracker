import math
from dataclasses import dataclass


class ObserverValidationError(Exception):
    """Raised when observer data is invalid."""



@dataclass(frozen=True)
class Observer:
    """
    Geodetic observer on Earth (WGS84 assumption at domain level).
    Attributes:

    latitude_deg: -90 to +90
    longitude_deg: -180 to +180
    altitude_m: meters above mean sea level
    """

    latitude_deg: float
    longitude_deg: float
    altitude_m: float

    def __post_init__(self):
        self._validate()

    # Validation logic

    def _validate(self):
        if not (-90.0 <= self.latitude_deg <= 90.0):
            raise ObserverValidationError(f"Latitude '{self.latitude_deg}' out of range [-90, 90]")

        if not (-180.0 <= self.longitude_deg <= 180.0):
            raise ObserverValidationError(f"Longitude '{self.longitude_deg}' out of range [-180, 180]")

        if not (-1000.0 <= self.altitude_m <= 100_000.0):
            raise ObserverValidationError(f"Altitude '{self.altitude_m}' out of range [-1000, 100000].")

    # Properties for internal use

    @property
    def latitude_rad(self) -> float:
        return math.radians(self.latitude_deg)

    @property
    def longitude_rad(self) -> float:
        return math.radians(self.longitude_deg)
