from dataclasses import dataclass

from numpy import double
from pyquaternion import Quaternion


@dataclass
class Location:
    x: float  # ECEF X coordinate in meters
    y: float  # ECEF Y coordinate in meters
    z: float  # ECEF Z coordinate in meters
    accuracy: float  # position accuracy in meters


@dataclass
class Position:
    """position of vehicle: location describes the location of the center of the rear axle; orientation is a
    quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, z+ = up"""

    location: Location
    orientation: Quaternion
