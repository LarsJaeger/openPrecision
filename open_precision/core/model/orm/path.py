from __future__ import annotations

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from open_precision.core.model.orm.orm_model_base import ORMModelBase
from open_precision.core.model.orm.waypoint import ORMWaypoint


class ORMPath(ORMModelBase):
    __tablename__ = 'Paths'

    id = Column(Integer, primary_key=True)

    priority = Column(Integer)
    waypoints = relationship(ORMWaypoint)
    course_id = Column(ForeignKey('Courses.id'))
