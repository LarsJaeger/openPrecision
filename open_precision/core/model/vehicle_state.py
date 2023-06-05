from dataclasses import dataclass

from neomodel import UniqueIdProperty, Property, StructuredNode

from open_precision.core.model import DataModelBase
from open_precision.core.model.position import Position, PositionProperty


@dataclass(kw_only=True)
class VehicleState(StructuredNode, DataModelBase):
    id: str = UniqueIdProperty()

    steering_angle: float | None = Property()  # in degrees, positive means clockwise (to the right if driving forward)
    speed: float | None = Property()  # in m/s, negative values mean reverse
    position: Position | None = PositionProperty()

    # TODO add fields for things like section control, implement state, etc.
