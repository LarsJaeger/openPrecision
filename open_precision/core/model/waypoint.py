from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from open_precision.core.model.model_base import Model
from open_precision.core.model.location import Location


@dataclass
class Waypoint(Model):
    # for SQLAlchemy purposes; __sa_dataclass_metadata_key__ is inherited from 'Model'-class
    __tablename__ = 'Waypoints'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})

    priority: int = field(init=True, default=0, metadata={'sa': Column(Integer)})  # higher priority = more important
    # and vice versa
    location: Location | None = field(init=True, default=None, metadata={'sa': relationship(Location, uselist=False)})
    path_id: int | None = field(init=False, default=None, repr=False, metadata={'sa': Column(ForeignKey('Paths.id'))})
