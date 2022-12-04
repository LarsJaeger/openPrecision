from __future__ import annotations

from dataclasses import field
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.persistence_model_base import PersistenceModelBase
from open_precision.core.model.waypoint import Waypoint

if TYPE_CHECKING:
    from open_precision.core.model.course import Course


class Path(DataModelBase, PersistenceModelBase):

    __tablename__ = "Paths"

    id: Mapped[int] = mapped_column(init=False, default=None, primary_key=True)

    priority: Mapped[int] = mapped_column(init=True, default=0)
    waypoints: List[Waypoint] = field(init=True, default_factory=list)
    _waypoints: Mapped[list[Waypoint]] = relationship(init=True, default_factory=list, repr=False, back_populates='path')
    course_id: Mapped[int] = mapped_column(ForeignKey("Courses.id"), init=True, repr=False, default=None)
    course: Mapped[Course] = relationship(default=None, init=True, uselist=False, back_populates='paths')

    def add_waypoint(self, waypoint: Waypoint) -> Path:
        waypoint.path = self
        self._waypoints.append(waypoint)
        return self

    @property
    def waypoints(self):
        return self._waypoints

    @waypoints.setter
    def waypoints(self, waypoints: list[Waypoint]):
        if isinstance(waypoints, list):
            for waypoint in waypoints:
                waypoint.path = self
            self._waypoints = waypoints
        else:
            self._waypoints = []