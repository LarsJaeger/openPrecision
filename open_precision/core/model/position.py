from dataclasses import dataclass
from pyquaternion import Quaternion


@dataclass
class Location:
    lat: float  # latitude in deg
    lon: float  # longitude in deg
    height: float  # returns height above sea level in mm
    horizontal_accuracy: int  # horizontal accuracy in mm
    vertical_accuracy: int  # vertical accuracy in mm


@dataclass
class Position:
    """position of vehicle: location describes the location of the center of the rear axle; orientation is a
    quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, z+ = up"""

    location: Location
    orientation: Quaternion
