from __future__ import annotations

from dataclasses import dataclass
from pyquaternion import Quaternion

from open_precision.core.model.location import Location


@dataclass(slots=True)
class Position:
    """position of vehicle: location describes the location of the center of the rear axle; orientation is a
    quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, z+ = up"""

    location: Location
    orientation: Quaternion

    def is_valid(self):
        return self.location.is_valid() and (self.orientation is not None)