from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from open_precision.core.model.data.data_model_base import DataModelBase
from open_precision.core.model.data.waypoint import Waypoint

if TYPE_CHECKING:
    from open_precision.core.model.data.course import Course


@dataclass
class Path(DataModelBase):
    id: int | None = field(init=False, default=None)

    priority: int = field(init=True, default=0)
    waypoints: list[Waypoint] = field(init=False, default_factory=list)
    course_id: Course.id = field(init=False, repr=False, default=None)

    def add_waypoint(self, waypoint: Waypoint) -> Path:
        waypoint.path = self
        self.waypoints.append(waypoint)
        return self
