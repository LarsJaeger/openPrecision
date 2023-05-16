from neomodel import StructuredNode, Property

from open_precision.core.model.data.data_model_base import DataModelBase


class Vehicle(StructuredNode, DataModelBase):
    name: str = Property(unique_index=True)
    turn_radius_left: float = Property(required=True)
    turn_radius_right: float = Property(required=True)
    wheelbase: float = Property(required=True)
    gps_receiver_offset: list[float] = Property(default=list([0., 0., 0.]))
