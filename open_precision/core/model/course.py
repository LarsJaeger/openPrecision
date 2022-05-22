from __future__ import annotations
from dataclasses import dataclass
from open_precision.core.exceptions import NotAPathException
from open_precision.core.model.path import Path


@dataclass
class Course:
    """ A course consists of paths that contain waypoints"""
    name: str
    description: str
    paths: list[Path]

    def add_path(self, path: Path):
        # check if Path has at least two waypoints
        if len(path.waypoints) < 2:
            raise NotAPathException
        path.course = self
        self.paths.append(path)
        return self
