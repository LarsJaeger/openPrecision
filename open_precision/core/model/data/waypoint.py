from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from open_precision.core.model.data.data_model_base import DataModelBase
from open_precision.core.model.data.location import Location
if TYPE_CHECKING:
    from open_precision.core.model.data.path import Path


@dataclass
class Waypoint(DataModelBase):

    id: int | None = field(init=False, default=None)

    priority: int = field(init=True, default=0)  # higher priority = more important
    # and vice versa
    location: Location | None = field(init=True, default=None)
    path_id: Path.id = field(init=False, default=None, repr=False)
