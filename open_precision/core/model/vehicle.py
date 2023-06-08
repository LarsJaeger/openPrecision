from dataclasses import dataclass

from neomodel import StructuredNode, Property

from open_precision.core.model import DataModelBase


@dataclass(kw_only=True)
class Vehicle(StructuredNode, DataModelBase):
    name: str = Property(unique_index=True)
    turn_radius_left: float = Property(required=True)
    turn_radius_right: float = Property(required=True)
    wheelbase: float = Property(required=True)
    gps_receiver_offset: list[float] = Property(default=list([0., 0., 0.]))
