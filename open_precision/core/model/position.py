from dataclasses import dataclass
import pyquaternion


@dataclass
class Location:
    lon: float  # longitude in deg
    lat: float  # latitude in deg
    height: int  # returns height above sea level in mm
    horizontal_accuracy: int  # horizontal accuracy in mm
    vertical_accuracy: int  # vertical accuracy in mm


@dataclass
class Orientation:
    orientation: pyquaternion


@dataclass
class Position:
    """position of vehicle: location describes the location of the center of the rear axle; orientation is a
    quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, z+ = up """
    location: Location
    orientation: Orientation
