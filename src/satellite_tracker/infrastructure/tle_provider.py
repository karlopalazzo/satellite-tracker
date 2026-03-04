import requests

CELESTRAK_URL = "https://celestrak.org/NORAD/elements/gp.php"


def get_satellite_tle(norad_id: int) -> tuple [str, str]:
    params = {
        "CATNR": norad_id,
        "FORMAT": "TLE"
    }

    response = requests.get(CELESTRAK_URL, params=params)
    response.raise_for_status()

    lines = response.text.strip().splitlines()

    tle_lines = [line for line in lines if line.startswith(("1", "2"))]

    if len(tle_lines) != 2:
        raise ValueError(f"TLE for NORAD {norad_id} not found.")

    return tle_lines[0], tle_lines[1]
