from __future__ import annotations

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from open_precision.core.model.orm.orm_model_base import ORMModelBase
from open_precision.core.model.orm.path import ORMPath


class ORMCourse(ORMModelBase):
    """ A course consists of paths that contain waypoints"""

    __tablename__ = 'Courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(400))
    paths = relationship(ORMPath)
