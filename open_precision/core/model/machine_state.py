from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, Float

from open_precision.core.model.model_base import Model


@dataclass
class MachineState(Model):
    # for SQLAlchemy purposes; __sa_dataclass_metadata_key__ is inherited from 'Model'-class
    __tablename__ = 'MachineStates'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})

    steering_angle: float = field(init=True, default=None, metadata={'sa': Column(Float())})  # in degrees, positive
    # means to the right
    speed: float = field(init=True, default=None, metadata={'sa': Column(Float())})  # in m/s, negative values mean
    # reverse
    # TODO add fields for things like section control, etc.