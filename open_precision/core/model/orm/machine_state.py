from sqlalchemy import Column, Integer, Float

from open_precision.core.model.orm.orm_model_base import ORMModelBase


class ORMMachineState(ORMModelBase):
    __tablename__ = 'MachineStates'

    id = Column(Integer, primary_key=True)
    steering_angle = Column(Float())
    speed = Column(Float())
