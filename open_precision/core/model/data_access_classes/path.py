from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from open_precision.core.model.data_classes.model_base import Model
from open_precision.core.model.data_classes.waypoint import Waypoint


class DAOPath:
    __tablename__ = 'Paths'

    id = Column(Integer, primary_key=True)

    priority = Column(Integer)
    waypoints = relationship(Waypoint)
    course_id = Column(ForeignKey('Courses.id'))
