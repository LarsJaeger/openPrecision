from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from open_precision.core.model.data_classes.model_base import Model
from open_precision.core.model.data_classes.waypoint import Waypoint


@dataclass
class Path(Model):
    id: int | None = field(init=False)

    priority: int = field(init=True, default=0)
    waypoints: list[Waypoint] = field(init=False, default_factory=list)
    course_id: id = field(init=False, repr=False)

    def add_waypoint(self, waypoint: Waypoint) -> Path:
        waypoint.path = self
        self.waypoints.append(waypoint)
        return self
