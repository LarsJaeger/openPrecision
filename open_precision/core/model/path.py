from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, registry

from open_precision.core.model.model import Model

if TYPE_CHECKING:
    from open_precision.core.model.course import Course
    from open_precision.core.model.waypoint import Waypoint


def start_mapping(mapper_registry):
    mapper_registry.mapped(Path)


mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Path(Model):
    # for SQLAlchemy purposes; __sa_dataclass_metadata_key__ is inherited from 'Model'-class
    __tablename__ = 'Paths'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})

    priority: int = field(init=True, default=0, metadata={'sa': Column(Integer)})
    waypoints: list[Waypoint] = field(init=False, default_factory=list, metadata={'sa': relationship('Waypoints')})
    course_id: id = field(init=False, repr=False, metadata={'sa': Column(ForeignKey('Courses.id'))})

    def add_waypoint(self, waypoint: Waypoint) -> Path:
        waypoint.path = self
        self.waypoints.append(waypoint)
        return self
