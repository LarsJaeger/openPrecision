from __future__ import annotations

import json
from dataclasses import field

import numpy as np
from sqlalchemy.orm import Mapped, mapped_column

from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.persistence_model_base import PersistenceModelBase


class Vehicle(DataModelBase, PersistenceModelBase):

    __tablename__ = "Vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    turn_radius_left: Mapped[float]
    turn_radius_right: Mapped[float]
    wheelbase: Mapped[float] # wheelbase in meters
    """3d vector from the rotation point of the vehicle (normally middle of the rear axle a tractor) at ground height 
    """
    gps_receiver_offset: np.ndarray | None = field(default=None)
    _gps_receiver_offset: Mapped[str] = mapped_column(init=False, default=None)

    @property
    def gps_receiver_offset(self) -> np.ndarray | None:
        print(f"loaded: {json.loads(self._gps_receiver_offset)}")
        print(f"loaded type: {type(json.loads(self._gps_receiver_offset))}")
        return np.array(json.loads(self._gps_receiver_offset), dtype=float)

    @gps_receiver_offset.setter
    def gps_receiver_offset(self, gps_receiver_offset: np.ndarray[float]):
        print(f"set: {json.dumps(gps_receiver_offset)}")
        self._gps_receiver_offset = json.dumps(gps_receiver_offset)