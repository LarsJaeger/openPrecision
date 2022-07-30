from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pyquaternion import Quaternion
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from open_precision.core.model.data_classes.location import Location
from open_precision.core.model.data_classes.model_base import Model


@dataclass
class Position(Model):
    """position of vehicle: location describes the location of the center of the rear axle; orientation is a
    quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, y+ = left, z+ = up"""

    id: int | None = field(init=False)

    location: Location | None
    orientation: Quaternion