from __future__ import annotations

from neomodel import UniqueIdProperty, StructuredNode, FloatProperty

from open_precision.core.model import DataModelBase
from open_precision.core.model.position import Position, PositionProperty


class VehicleState(DataModelBase, StructuredNode):
	uuid: str = UniqueIdProperty()

	steering_angle: float | None = (
		FloatProperty()
	)  # in degrees, positive means clockwise (to the right if driving forward)
	speed: float | None = FloatProperty()  # in m/s, negative values mean reverse
	position: Position | None = PositionProperty()


# TODO add fields for things like section control, implement state, etc.
