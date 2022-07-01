from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from open_precision.core.model.course import Course
    from open_precision.core.model.waypoint import Waypoint


@dataclass(slots=True)
class Path:
    priority: int = field(init=True, default=0)
    waypoints: list[Waypoint] = field(init=False, default_factory=lambda: [])
    course: Course | None = field(init=False, default=None, repr=False)

    def add_waypoint(self, waypoint: Waypoint) -> Path:
        waypoint.path = self
        self.waypoints.append(waypoint)
        return self

    @property
    def id(self) -> int:
        """ Attention: Very resource intensive; gets index from search of current course's path list"""
        return self.course.paths.index(self)
