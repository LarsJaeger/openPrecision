from __future__ import annotations

from typing import TYPE_CHECKING

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
    waypoints: Mapped[list[Waypoint]] = relationship(init=False, default_factory=list, back_populates='path')
    course_id: Mapped[int] = mapped_column(ForeignKey("Courses.id"), init=False, repr=False, default=None)
    course: Mapped[Course] = relationship(default=None, init=False)

    #TODO setter for waypoints

    def add_waypoint(self, waypoint: Waypoint) -> Path:
        waypoint.path = self
        self.waypoints.append(waypoint)
        return self
