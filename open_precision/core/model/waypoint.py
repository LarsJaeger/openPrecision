from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, registry

from open_precision.core.model.model import Model

if TYPE_CHECKING:
    from open_precision.core.model.path import Path
    from open_precision.core.model.location import Location


def start_mapping(mapper_registry):
    mapper_registry.mapped(Waypoint)


mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Waypoint(Model):
    # for SQLAlchemy purposes; __sa_dataclass_metadata_key__ is inherited from 'Model'-class
    __tablename__ = 'Waypoints'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})

    priority: int = field(init=True, default=0, metadata={'sa': Column(Integer)})  # higher priority = more important and vice versa
    location: Location | None = field(init=True, default=None, metadata={'sa': relationship('Locations')})
    path_id: int | None = field(init=False, default=None, repr=False, metadata={'sa': Column(ForeignKey('Paths.id'))})