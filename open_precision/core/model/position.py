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
    """position of vehicle: location describes the location of the center of the rear axle; orientation is quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, z+ = up"""
    location: Location
    orientation: Orientation
