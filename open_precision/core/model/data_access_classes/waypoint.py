from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from open_precision.core.model.data_classes.model_base import Model
from open_precision.core.model.data_classes.location import Location


class DAOWaypoint:
    __tablename__ = 'Waypoints'

    id = Column(Integer, primary_key=True)

    priority = Column(Integer)
    # and vice versa
    location = relationship(Location, uselist=False)
    path_id = Column(ForeignKey('Paths.id'))
