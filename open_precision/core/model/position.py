from dataclasses import dataclass, field
from math import sqrt

import numpy as np
from numpy import double
from pyquaternion import Quaternion


@dataclass
class Location:
    x: float  # ECEF X coordinate in meters
    y: float  # ECEF Y coordinate in meters
    z: float  # ECEF Z coordinate in meters
    error: float  # position accuracy in meters

    def __add__(self, other):
        if isinstance(other, Location):
            self.x += other.x
            self.y += other.y
            self.z += other.z
            self.error += other.error
        elif isinstance(other, list) or isinstance(other, tuple):
            if 3 <= len(other) <= 4:
                floated_vals = [float(i) for i in other]
                self.x += other[0]
                self.y += other[1]
                self.z += other[2]
                if len(other) == 4:
                    self.error += other[3]
        return self

    def __sub__(self, other):
        if isinstance(other, Location):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
            self.error += other.error
        elif isinstance(other, list) or isinstance(other, tuple):
            if 3 <= len(other) <= 4:
                floated_vals = [float(i) for i in other]
                self.x -= other[0]
                self.y -= other[1]
                self.z -= other[2]
                if len(other) == 4:
                    self.error += other[3]
        return self

    def __abs__(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2 + self.y ** 2)

    def to_numpy(self) -> np.ndarray:
        return np.ndarray([self.x, self.y, self.z])

@dataclass
class Position:
    """position of vehicle: location describes the location of the center of the rear axle; orientation is a
    quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, z+ = up"""

    location: Location
    orientation: Quaternion
