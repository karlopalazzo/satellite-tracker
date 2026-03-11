# Satellite Tracker

Python project for tracking satellites using TLE data and SGP4 propagation.

## Features

- TLE parsing
- SGP4 propagation
- Coordinate transformations:
  - ECI
  - ECEF
  - ENU
- Azimuth / Elevation / Range calculation
- Multi-satellite tracking

## How it works

The tracking pipeline follows the standard astrodynamics transformation chain:

1. **TLE propagation** using the SGP4 algorithm
2. Satellite position computed in the **ECI frame**
3. Transformation to **ECEF** using Greenwich Mean Sidereal Time
4. Conversion to **topocentric ENU frame** relative to the observer
5. Computation of **Azimuth, Elevation and Range**

TLE
 ↓
SGP4 propagation
 ↓
ECI coordinates
 ↓
ECEF coordinates
 ↓
Topocentric ENU
 ↓
Azimuth / Elevation / Range

## Requirements

- Python 3.10+

## Installation

```bash
pip install -e .
```

## Run

```
python -m satellite_tracker
```

## Project structure

satellite-tracker/
│
├── pyproject.toml
├── README.md
├── .gitignore
│
├── src/
│ └── satellite_tracker/
│ ├── main.py
│ ├── calc/
│ │ ├── frames.py
│ │ ├── propagator.py
│ │ └── topocentric.py
│ │
│ ├── domain/
│ │ ├── observer.py
│ │ ├── tracker.py
│ │ └── constellation_tracker.py
│ │
│ └── infrastructure/
│ └── tle_provider.py
│
└── tests/

## Pipeline diagram
TLE → SGP4 → ECI → ECEF → ENU → Az/El

## Example output

ISS
Az: 248.31° El: 1.10° Range: 2256151 m
Visible

Hubble
Az: 247.79° El: -15.09° Range: 4670344 m
Below horizon