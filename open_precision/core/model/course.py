from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from open_precision.core.exceptions import NotAPathException

if TYPE_CHECKING:
    from open_precision.core.model.path import Path


@dataclass(slots=True)
class Course:
    """ A course consists of paths that contain waypoints"""
    name: str = field(init=True, default=None)
    description: str = field(init=True, default=None)
    paths: list[Path] = field(init=False, default_factory=lambda: [])

    def add_path(self, path: Path):
        # check if Path has at least two waypoints
        if len(path.waypoints) < 2:
            raise NotAPathException(path)
        path.course = self
        self.paths.append(path)
        return self
