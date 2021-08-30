from dataclasses import dataclass
import pyquaternion


@dataclass
class Location:
    lon: float
    lat: float
    height: float


@dataclass
class Orientation:
    orientation: pyquaternion


@dataclass
class Position:
    location: Location
    orientation: Orientation
