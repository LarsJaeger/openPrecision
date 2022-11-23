from __future__ import annotations

import json
from dataclasses import field

from pyquaternion import Quaternion
from sqlalchemy.orm import mapped_column, Mapped

from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.location import Location
from open_precision.core.model.orientation import Orientation
from open_precision.core.model.persistence_model_base import PersistenceModelBase


class Position(DataModelBase, PersistenceModelBase):
    """position of vehicle: location describes the location of the center of the rear axle; orientation is a
    quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, y+ = left, z+ = up"""

    __tablename__ = "Positions"

    id: Mapped[int] = mapped_column(init=False, default=None, primary_key=True)

    location: Location | None = field(default=None)
    _location: Mapped[str] = mapped_column(init=False, default=None, repr=False)

    orientation: Orientation | None = field(default=None)
    _orientation: Mapped[str] = mapped_column(init=False, default=None)

    @property
    def location(self) -> Location | None:
        return Location(**json.loads(self._location))

    @location.setter
    def location(self, location: Location):
        self._location = location.to_json()

    @property
    def orientation(self) -> Orientation | None:
        return Orientation(**json.loads(self._orientation))

    @orientation.setter
    def orientation(self, orientation: Orientation):
        if (not isinstance(orientation, Orientation)) and isinstance(orientation, Quaternion):
            orientation = Orientation(orientation)
        self._orientation = orientation.to_json()

    def is_valid(self):
        return self.location.is_valid() and (self.orientation is not None)
