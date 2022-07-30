from __future__ import annotations

import ast
from dataclasses import dataclass, field

from sqlalchemy import Column, String, Float, Integer

from open_precision.core.model.data_classes.model_base import Model


@dataclass
class Vehicle(Model):
    id: int
    name: str
    turn_radius_left: float
    turn_radius_right: float
    wheelbase: float # wheelbase in meters
    """3d vector from the rotation point of the vehicle (normally middle of the rear axle a tractor) at ground height 
    """
    gps_receiver_offset: list[float]