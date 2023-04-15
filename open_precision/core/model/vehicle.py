from __future__ import annotations

import json
from dataclasses import field

import numpy as np
from sqlalchemy.orm import Mapped, mapped_column

from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.persistence_model_base import PersistenceModelBase


class Vehicle(DataModelBase, PersistenceModelBase):

    __tablename__ = "Vehicles"

    id: Mapped[int] = mapped_column(init=True, primary_key=True, default=None)

    name: Mapped[str] = mapped_column(init=True, default=None)
    turn_radius_left: Mapped[float] = mapped_column(init=True, default=None)
    turn_radius_right: Mapped[float] = mapped_column(init=True, default=None)
    wheelbase: Mapped[float] = mapped_column(init=True, default=None) # wheelbase in meters
    """3d vector from the rotation point of the vehicle (normally middle of the rear axle a tractor) at ground height 
    """
    gps_receiver_offset: np.ndarray | None = field(init=True, default=None)
    _gps_receiver_offset: Mapped[str] = mapped_column(init=True, default=None, nullable=True)

    @property
    def gps_receiver_offset(self) -> np.ndarray | None:
        return np.array(json.loads(self._gps_receiver_offset), dtype=float) if self._gps_receiver_offset else None

    @gps_receiver_offset.setter
    def gps_receiver_offset(self, gps_receiver_offset: np.ndarray[float]):
        if type(gps_receiver_offset) is property:
            #  initial value not specified, use default TODO create seperate setter decorator to integrate this with
            #  the model
            gps_receiver_offset = Vehicle._gps_receiver_offset
        if type(gps_receiver_offset) is np.ndarray:
            gps_receiver_offset = gps_receiver_offset.tolist()
        self._gps_receiver_offset = json.dumps(gps_receiver_offset)