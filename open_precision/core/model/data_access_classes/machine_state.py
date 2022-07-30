from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, Float

from open_precision.core.model.data_classes.model_base import Model


class DAOMachineState:
    __tablename__ = 'MachineStates'

    id = Column(Integer, primary_key=True)
    steering_angle = Column(Float())
    speed = Column(Float())