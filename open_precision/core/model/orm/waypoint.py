from __future__ import annotations

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from open_precision.core.model.orm.location import ORMLocation
from open_precision.core.model.orm.orm_model_base import ORMModelBase


class ORMWaypoint(ORMModelBase):
    __tablename__ = 'Waypoints'

    id = Column(Integer, primary_key=True)

    priority = Column(Integer)
    location = relationship(ORMLocation, uselist=False)
    path_id = Column(ForeignKey('Paths.id'))
