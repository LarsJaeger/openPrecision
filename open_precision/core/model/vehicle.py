from __future__ import annotations
from dataclasses import dataclass


@dataclass(slots=True)
class Vehicle:
    name: str
    gps_receiver_offset: list
    """ 3d vector from the rotation point of the vehicle (normally middle of the rear axle a tractor) at ground height"""
    turn_radius_left: float
    turn_radius_right: float
    wheelbase: float  # wheelbase in meters
