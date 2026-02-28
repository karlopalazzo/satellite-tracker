import requests

CELESTRAK_URL = "https://celestrak.org/NORAD/elements/stations.txt"
ISS_NORAD_ID = "25544"

def get_iss_tle() -> tuple [str, str]:
    response = requests.get(CELESTRAK_URL)
    response.raise_for_status()

    lines = response.text.splitlines()

    for i in range(len(lines)):
        if ISS_NORAD_ID in lines[i]:
            return lines[i], lines[i+1]
    
    raise ValueError("ISS TLE not found.")