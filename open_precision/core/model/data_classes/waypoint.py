from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from open_precision.core.model.data_classes.model_base import Model
from open_precision.core.model.data_classes.location import Location


@dataclass
class Waypoint(Model):

    id: int | None = field(init=False)

    priority: int = field(init=True, default=0)  # higher priority = more important
    # and vice versa
    location: Location | None = field(init=True, default=None)
    path_id: int | None = field(init=False, default=None, repr=False)
