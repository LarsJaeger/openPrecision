from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from open_precision.core.exceptions import NotAPathException
from open_precision.core.model.data_classes.model_base import Model
from open_precision.core.model.data_classes.path import Path


class DAOCourse:
    """ A course consists of paths that contain waypoints"""

    __tablename__ = 'Courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(400))
    paths = relationship(Path)
