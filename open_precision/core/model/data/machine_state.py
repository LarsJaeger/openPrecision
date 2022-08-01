from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, Float

from open_precision.core.model.data.data_model_base import DataModelBase


@dataclass
class MachineState(DataModelBase):

    id: int | None = field(init=False, default=None)

    steering_angle: float = field(init=True, default=None)  # in degrees, positive
    # means to the right
    speed: float = field(init=True, default=None)  # in m/s, negative values mean
    # reverse
    # TODO add fields for things like section control, etc.