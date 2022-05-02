from dataclasses import dataclass, field

from open_precision.core.model.path import Path
from open_precision.core.model.waypoint import Waypoint


@dataclass
class Course:
    """ A course consists of paths that contain waypoints"""
    name: str
    description: str
    paths: list[Path]

    def add_path(self, path: Path):
        # check if Path has at least two waypoints
        if len(path.waypoints) < 2:
            raise PathError
        path.course = self
        self.paths.append(path)
        return self
