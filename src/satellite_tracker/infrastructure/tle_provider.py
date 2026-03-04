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

    if len(lines) < 2:
        raise ValueError(f"TLE for NORAD {norad_id} not found.")

    return lines[0], lines[1]
