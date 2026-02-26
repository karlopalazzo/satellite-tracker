import pytest
from datetime import datetime
from iss_tracker.domain.tle import TLEParser, TLEParseError


NAME = "ISS (ZARYA)"
LINE1 = "1 25544U 98067A   26057.54172094  .00011988  00000+0  23066-3 0  9998"
LINE2 = 2 25544  51.6322 127.4658 0008344 135.8715 224.2940 15.48311551554600"


def test_parse_valid_tle():
    tle = TLEParser.parse_tle(NAME, LINE1, LINE2)

    assert tle.name == "ISS (ZARYA)"
    assert tle.norad_id == 25544
    assert tle.classification == "U"
    assert tle.international_designator == "98067A"

    assert tle.inclination == pytest.approx(51.6322)
    assert tle.right_ascension == pytest.approx(127.4658)
    assert tle.eccentricity == pytest.approx(0.0008344)
    assert tle.mean_motion_rev_per_day == pytest.approx(15.48311551)

    # Epoch sanity checks
    assert isinstance(tle.epoch, datetime)
    assert tle.epoch.year == 2026


def test_invalid_length():
    with pytest.raises(TLEParseError):
        TLEParser.parse(NAME, LINE1[:-1], LINE2)


def test_invalid_checksum():
    bad_line1 = LINE1[:-1] + "0"  # Changing checksum to an incorrect value"
    with pytest.raises(TLEParseError):
        TLEParser.parse(NAME, bad_line1, LINE2)


def test_norad_mismatch():
    bad_line2 = "2 12345  51.6417  18.9245 0004767  67.8172  52.6823 15.50336457438218"
    with pytest.raises(TLEParseError):
        TLEParser.parse(NAME, LINE1, bad_line2)


def test_invalid_line_numbers():
    bad_line1 = "9" + LINE1[1:]
    with pytest.raises(TLEParseError):
        TLEParser.parse(NAME, bad_line1, LINE2)
