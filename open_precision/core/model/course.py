from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String

from open_precision.core.exceptions import NotAPathException
from open_precision.core.model.model import Model

if TYPE_CHECKING:
    from open_precision.core.model.path import Path


@dataclass
class Course(Model):
    """ A course consists of paths that contain waypoints"""

    # for SQLAlchemy purposes, __sa_dataclass_metadata_key__ is inherited from 'Model'-class
    __tablename__ = 'user'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})

    name: str = field(init=True, default=None, metadata={'sa': Column(String(50))})
    description: str = field(init=True, default=None, metadata={'sa': Column(String(400))})
    paths: list[Path] = field(init=False, default_factory=lambda: [], metadata={'sa': relationship('')})

    def add_path(self, path: Path):
        # check if Path has at least two waypoints
        if len(path.waypoints) < 2:
            raise NotAPathException(path)
        path.course = self
        self.paths.append(path)
        return self
