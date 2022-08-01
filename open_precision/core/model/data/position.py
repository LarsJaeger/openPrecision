from __future__ import annotations

from dataclasses import dataclass, field

from pyquaternion import Quaternion

from open_precision.core.model.data.data_model_base import DataModelBase
from open_precision.core.model.data.location import Location


@dataclass
class Position(DataModelBase):
    """position of vehicle: location describes the location of the center of the rear axle; orientation is a
    quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, y+ = left, z+ = up"""

    id: int | None = field(init=False, default=None)

    location: Location | None
    orientation: Quaternion

    def is_valid(self):
        return self.location.is_valid() and (self.orientation is not None)
