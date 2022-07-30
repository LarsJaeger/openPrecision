from __future__ import annotations

import ast
from dataclasses import dataclass, field

from sqlalchemy import Column, String, Float, Integer

from open_precision.core.model.data_classes.model_base import Model


class DAOVehicle:
    __tablename__ = 'Vehicles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    turn_radius_left = Column(Float())
    turn_radius_right = Column(Float())
    wheelbase = Column(Float())
    gps_receiver_offset = Column(String(50))