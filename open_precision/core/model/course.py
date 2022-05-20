from dataclasses import dataclass

from open_precision.core.exceptions import NotAPathException
from open_precision.core.model import path


@dataclass
class Course:
    """ A course consists of paths that contain waypoints"""
    name: str
    description: str
    paths: list[path.Path]

    def add_path(self, path: path.Path):
        # check if Path has at least two waypoints
        if len(path.waypoints) < 2:
            raise NotAPathException
        path.course = self
        self.paths.append(path)
        return self
