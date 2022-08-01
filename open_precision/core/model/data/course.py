from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from open_precision.core.exceptions import NotAPathException
from open_precision.core.model.data.data_model_base import DataModelBase
from open_precision.core.model.data.path import Path

if TYPE_CHECKING:
    pass


@dataclass
class Course(DataModelBase):
    """ A course consists of paths that contain waypoints"""
    id: int | None = field(init=False, default=None)

    name: str = field(init=True, default=None)
    description: str = field(init=True, default=None)
    paths: list[Path] = field(init=False, default_factory=list)

    def add_path(self, path: Path):
        # check if Path has at least two waypoints
        if len(path.waypoints) < 2:
            raise NotAPathException(path)
        path.course = self
        self.paths.append(path)
        return self

