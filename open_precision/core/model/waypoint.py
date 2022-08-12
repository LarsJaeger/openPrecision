from __future__ import annotations

import json
from dataclasses import field
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from open_precision.core.model.data_model_base import DataModelBase
from open_precision.core.model.location import Location
from open_precision.core.model.persistence_model_base import PersistenceModelBase

if TYPE_CHECKING:
    from open_precision.core.model.path import Path


class Waypoint(DataModelBase, PersistenceModelBase):
    __tablename__ = "Waypoints"

    id: Mapped[int] = mapped_column(init=False, default=None, primary_key=True)

    priority: Mapped[int] = mapped_column(init=True, default=0)  # higher priority = more important
    # and vice versa

    location: Location | None = field(default=None)
    _location: Mapped[str] = mapped_column(init=False, default=None)

    path_id: Mapped[int] = mapped_column(ForeignKey("Paths.id"), init=False, default=None, repr=False)
    path: Mapped[Path] = relationship(default=None, init=False)

    @property
    def location(self) -> Location | None:
        return Location(**json.loads(self._location))

    @location.setter
    def location(self, location: Location):
        self._location = location.as_json()