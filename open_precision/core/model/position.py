from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
import numpy as np
from pyquaternion import Quaternion


@dataclass(slots=True)
class Location:
    x: float  # ECEF X coordinate in meters
    y: float  # ECEF Y coordinate in meters
    z: float  # ECEF Z coordinate in meters
    error: 'float'  # position accuracy in meters

    def __add__(self, other):
        if isinstance(other, Location):
            self.x += other.x
            self.y += other.y
            self.z += other.z
            self.error += other.error
        elif isinstance(other, list) \
                or isinstance(other, tuple):
            if 3 <= len(other) <= 4:
                floated_vals = [float(i) for i in other]
                self.x += other[0]
                self.y += other[1]
                self.z += other[2]
                if len(other) == 4:
                    self.error += other[3]
            else:
                raise TypeError
        elif isinstance(other, np.ndarray):
            print("hello there")
            if 3 <= other.shape[0] <= 4:
                floated_vals = [float(i) for i in other]
                self.x += other[0]
                self.y += other[1]
                self.z += other[2]
                if len(other) == 4:
                    self.error += other[3]
        else:
            raise TypeError

        return self

    def __sub__(self, other):
        if isinstance(other, Location):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
            self.error += other.error
        elif isinstance(other, list) or isinstance(other, tuple) or isinstance(other, np.ndarray):
            if 3 <= len(other) <= 4:
                floated_vals = [float(i) for i in other]
                self.x -= other[0]
                self.y -= other[1]
                self.z -= other[2]
                if len(other) == 4:
                    self.error += other[3]
        else:
            raise TypeError
        return self

    def to_numpy(self) -> np.array:
        return np.array([self.x, self.y, self.z], dtype=np.float64)


@dataclass(slots=True)
class Position:
    """position of vehicle: location describes the location of the center of the rear axle; orientation is a
    quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, z+ = up"""

    location: Location
    orientation: Quaternion
