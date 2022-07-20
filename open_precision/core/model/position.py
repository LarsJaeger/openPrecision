from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pyquaternion import Quaternion
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from open_precision.core.model.location import Location
from open_precision.core.model.model_base import Model


@dataclass
class Position(Model):
    """position of vehicle: location describes the location of the center of the rear axle; orientation is a
    quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, y+ = left, z+ = up"""

    # for SQLAlchemy purposes; __sa_dataclass_metadata_key__ is inherited from 'Model'-class
    __tablename__ = 'Positions'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})

    location: Location | None = field(metadata={'sa': relationship(Location)})
    _orientation = Column(String(50))
    orientation: Quaternion

    @property
    def orientation(self) -> Quaternion:
        return Quaternion(ast.literal_eval(self._orientation))

    @orientation.setter
    def orientation(self, orientation: Quaternion) -> None:
        self._orientation = repr(orientation)
