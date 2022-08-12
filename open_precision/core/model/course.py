from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, Mapped, mapped_column

from open_precision.core.exceptions import NotAPathException
from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.path import Path
from open_precision.core.model.persistence_model_base import PersistenceModelBase

if TYPE_CHECKING:
    pass


class Course(DataModelBase, PersistenceModelBase):
    __tablename__ = "Courses"

    """ A course consists of paths that contain waypoints"""
    id: Mapped[int] = mapped_column(init=False, default=None, primary_key=True)

    name: Mapped[str] = mapped_column(init=True, default=None)
    description: Mapped[str] = mapped_column(init=True, default=None, nullable=True)
    paths: Mapped[list[Path]] = relationship(default_factory=list, back_populates='course')

    #TODO setter for paths

    def add_path(self, path: Path):
        # check if Path has at least two waypoints
        if len(path.waypoints) < 2:
            raise NotAPathException(path)
        path.course = self
        self.paths.append(path)
        return self
