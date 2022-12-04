from __future__ import annotations

import json
from dataclasses import field
from typing import TYPE_CHECKING

from pyquaternion import Quaternion
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.location import Location
from open_precision.core.model.orientation import Orientation
from open_precision.core.model.persistence_model_base import PersistenceModelBase

if TYPE_CHECKING:
    from open_precision.core.model.machine_state import MachineState


class Position(DataModelBase, PersistenceModelBase):
    """position of vehicle: location describes the location of the center of the rear axle; orientation is a
    quaternion describing rotation from x+ = north, z- = gravity to x+ = main driving direction, y+ = left, z+ = up"""

    __tablename__ = "Positions"

    id: Mapped[int] = mapped_column(init=True, default=None, primary_key=True)

    location: Location | None = field(init=True, default=None)
    _location: Mapped[str] = mapped_column(init=True, default=None, repr=False)

    orientation: Orientation | None = field(init=True, default=None)
    _orientation: Mapped[str] = mapped_column(init=True, default=None, repr=False)

    machine_state: Mapped[MachineState] = relationship(init=True, default=None, uselist=False, repr=False, back_populates="position")  # in JSON format

    @property
    def location(self) -> Location | None:
        return Location(**json.loads(self._location)) # TODO update to use .from_json() method

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
