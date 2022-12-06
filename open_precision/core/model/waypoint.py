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

    id: Mapped[int] = mapped_column(init=True, default=None, primary_key=True)

    priority: Mapped[int] = mapped_column(init=True, default=None)  # higher priority = more important
    # and vice versa

    location: Location | None = field(init=True, default=None)
    _location: Mapped[str] = mapped_column(init=True, default=None)

    path_id: Mapped[int] = mapped_column(ForeignKey("Paths.id"), init=True, default=None)
    path: Mapped[Path] = relationship(init=True, default=None)

    @property
    def location(self) -> Location | None:
        return Location(**json.loads(self._location))

    @location.setter
    def location(self, location: Location):
        self._location = location.to_json()
