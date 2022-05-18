from dataclasses import dataclass, field

from open_precision.core.model.course import Course
from open_precision.core.model.waypoint import Waypoint


class Path:
    pass


@dataclass
class Path:
    priority: int = field(init=True, default=0)
    waypoints: list[Waypoint] = field(init=True, default_factory=lambda: [])
    course: Course = field(init=False, default=None)

    def add_waypoint(self, waypoint) -> Path:
        waypoint.path = self
        self.waypoints.append(waypoint)
        return self

    @property
    def id(self) -> int:
        """ Attention: Very resource intensive; gets index from search of current course's path list"""
        return self.course.paths.index(self)
