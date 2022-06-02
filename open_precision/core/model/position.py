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
        match other:
            case Location():
                res_x = self.x + other.x
                res_y = self.y + other.y
                res_z = self.z + other.z
                res_error = self.error + other.error
            case list() | tuple():
                if 3 <= len(other) <= 4 \
                        and self.error is not None \
                        and other.error is not None:
                    floated_vals = [float(i) for i in other]
                    res_x = self.x + other[0]
                    res_y = self.y + other[1]
                    res_z = self.z + other[2]
                else:
                    raise TypeError
                if len(other) == 4:
                    res_error = self.error + other[3]
                else:
                    res_error = None

            case np.ndarray():
                if 3 <= other.shape[0] <= 4:
                    floated_vals = [float(i) for i in other]
                    res_x = self.x + other[0]
                    res_y = self.y + other[1]
                    res_z = self.z + other[2]
                else:
                    raise TypeError
                if len(other) == 4 \
                        and self.error is not None \
                        and other.error is not None:
                    res_error = self.error + other[3]
                else:
                    res_error = None
            case _: raise TypeError
        return Location(x=res_x, y=res_y, z=res_z, error=res_error)

    def __sub__(self, other):
        match other:
            case Location():
                res_x = self.x - other.x
                res_y = self.y - other.y
                res_z = self.z - other.z
                res_error = self.error + other.error
            case list() | tuple():
                if 3 <= len(other) <= 4:
                    floated_vals = [float(i) for i in other]
                    res_x = self.x - other[0]
                    res_y = self.y - other[1]
                    res_z = self.z - other[2]
                else:
                    raise TypeError
                if len(other) == 4 \
                        and self.error is not None \
                        and other.error is not None:
                    res_error = self.error - other[3]
                else:
                    res_error = None

            case np.ndarray():
                if 3 <= other.shape[0] <= 4:
                    floated_vals = [float(i) for i in other]
                    res_x = self.x - other[0]
                    res_y = self.y - other[1]
                    res_z = self.z - other[2]
                else:
                    raise TypeError
                if len(other) == 4 \
                        and self.error is not None \
                        and other.error is not None:
                    res_error = self.error + other[3]
                else:
                    res_error = None
            case _:
                raise TypeError
        return Location(x=res_x, y=res_y, z=res_z, error=res_error)

    def to_numpy(self) -> np.array:
        return np.array([self.x, self.y, self.z], dtype=np.float64)


@dataclass(slots=True)
class Position:
    """position of vehicle: location describes the location of the center of the rear axle; orientation is a
    quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, z+ = up"""

    location: Location
    orientation: Quaternion
