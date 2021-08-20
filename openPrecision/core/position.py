from dataclasses import dataclass

import numpy as np


@dataclass
class Location:
    lon: float
    lat: float
    height: float


@dataclass
class Orientation:
    ypr: np.array


@dataclass
class Position:
    location: Location
    orientation: Orientation
