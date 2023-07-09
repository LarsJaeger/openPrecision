from __future__ import annotations

from dataclasses import dataclass

from neomodel import StructuredNode, Property, StringProperty, FloatProperty, ArrayProperty

from open_precision.core.model import DataModelBase


class Vehicle(StructuredNode, DataModelBase):
    name: str = StringProperty(unique_index=True)
    turn_radius_left: float = FloatProperty(required=True)
    turn_radius_right: float = FloatProperty(required=True)
    wheelbase: float = FloatProperty(required=True)
    gps_receiver_offset: list[float] = ArrayProperty(default=list([0., 0., 0.]))
