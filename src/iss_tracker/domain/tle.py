from dataclasses import dataclass
from datetime import datetime, timezone, timedelta


class TLEParseError(Exception):
    """Exception class for TLE parsing errors."""
    pass


@dataclass(frozen=True)  # frozen==immutable
class TLE:
    """Two-Line Element set (TLE) for satellite tracking."""
    name: str
    
    # Line 1 information:
    norad_id: int
    classification: str
    international_designator: str
    epoch: datetime
    mean_motion_derivative: float
    mean_motion_sec_derivative: float
    bstar: float
    ephemeris_type: int
    element_set_number: int

    # Line 2 information:
    inclination: float
    right_ascension: float
    eccentricity: float
    argument_of_perigee: float
    mean_anomaly_deg: float
    mean_motion_rev_per_day: float
    rev_num_at_epoch: int


class TLEParser:
    """Parser for Two-Line Element sets (TLE)."""

    @staticmethod
    def parse_tle(name: str, line1: str, line2: str) -> TLE:
        """Parse TLE lines (str) and return a TLE object."""
        TLEParser._validate_lines(line1, line2)
        TLEParser._validate_line_numbers(line1, line2)
        TLEParser._validate_norad_consistency(line1, line2)
        TLEParser._validate_checksum(line1)
        TLEParser._validate_checksum(line2)

        # Extract fields from line 1
        norad_id = int(line1[2:7])
        classification = line1[7]
        international_designator = line1[9:17].strip()
        epoch = TLEParser._parse_epoch(line1)
        mean_motion_derivative = float(line1[33:43].strip())
        mean_motion_sec_derivative = TLEParser._parse_exponent_field(line1[44:52])
        bstar = TLEParser._parse_exponent_field(line1[53:61])
        ephemeris_type = int(line1[62])
        element_set_number = int(line1[64:68])

        # Extract fields from line 2
        inclination = float(line2[8:16])
        right_ascension = float(line2[17:25])
        eccentricity = float("0." + line2[26:33].strip())
        argument_of_perigee = float(line2[34:42])
        mean_anomaly_deg = float(line2[43:51])
        mean_motion_rev_per_day = float(line2[52:63])
        rev_num_at_epoch = int(line2[63:68])

        return TLE(
            name=name.strip(),
            norad_id=norad_id,
            classification=classification,
            international_designator=international_designator,
            epoch=epoch,
            mean_motion_derivative=mean_motion_derivative,
            mean_motion_sec_derivative=mean_motion_sec_derivative,
            bstar=bstar,
            ephemeris_type=ephemeris_type,
            element_set_number=element_set_number,
            inclination=inclination,
            right_ascension=right_ascension,
            eccentricity=eccentricity,
            argument_of_perigee=argument_of_perigee,
            mean_anomaly_deg=mean_anomaly_deg,
            mean_motion_rev_per_day=mean_motion_rev_per_day,
            rev_num_at_epoch=rev_num_at_epoch,
        )

# Validation methods for TLE lines

    @staticmethod
    def _validate_lines(line1: str, line2: str):
        if len(line1) != 69 or len(line2) != 69:
            raise TLEParseError(f"Each TLE line must be exactly 69 characters. L1: {len(line1)}, L2: {len(line2)}")

    @staticmethod
    def _validate_line_numbers(line1: str, line2: str):
        if not line1.startswith("1 ") or not line2.startswith("2 "):
            raise TLEParseError(f"TLE lines must start with '1 ' and '2 '. L1: '{line1[:2]}', L2: '{line2[:2]}'")

    @staticmethod
    def _validate_norad_consistency(line1: str, line2: str):
        if line1[2:7] != line2[2:7]:
            raise TLEParseError(f"NORAD ID mismatch between lines. L1: {line1[2:7]}, L2: {line2[2:7]}")

    @staticmethod
    def _validate_checksum(line: str):
        expected = int(line[-1])
        calculated = TLEParser._calculate_checksum(line)
        if expected != calculated:
            raise TLEParseError(f"Checksum mismatch. Expected: '{expected}', Calculated: '{calculated}'")

    @staticmethod
    def _calculate_checksum(line: str) -> int:
        '''Calculate the checksum to confirm integrity of the TLE line. 
        Results in a single digit (0-9) using modulo 10 on final sum.'''
        checksum = 0
        for char in line[:-1]:  # Checksum char is excluded
            if char.isdigit():
                checksum += int(char)
            elif char == "-":  # Negative sign counts as 1
                checksum += 1
        return checksum % 10

# Helper method to parse the epoch field from line 1

    @staticmethod
    def _parse_epoch(line1: str) -> datetime:
        '''Parse the epoch field from line 1,
        returning a timezone-aware datetime object in UTC.'''
        year = int(line1[18:20])
        day_of_year = float(line1[20:32].strip())

        full_year = 1900 + year if year >= 57 else 2000 + year  # 1957-1999 or 2000-2056
        return datetime(full_year, 1, 1, tzinfo=timezone.utc) + timedelta(days=day_of_year - 1)

    @staticmethod
    def _parse_exponent_field(field: str) -> float:
        '''Parse fields that use a compact scientific notation,
        returning the corresponding float value.'''
        field = field.strip()
        
        if not field:
            return 0.0  # Treat empty fields as zero

        sign = -1 if field.startswith("-") else 1

        if field[0] in "-+":
            field = field[1:]
        
        mantissa = float(f"0.{field[0:5]}")
        exponent = int(field[5:])

        return sign * mantissa * (10 ** exponent)