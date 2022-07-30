from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from sqlalchemy import Column, Float, Integer, ForeignKey

from open_precision.core.model.data_classes.model_base import Model


class DAOLocation:
    __tablename__ = 'Locations'

    id = Column(Integer, primary_key=True)
    position_id = Column(ForeignKey('Positions.id'))
    waypoint_id = Column(ForeignKey('Waypoints.id'))

    x = Column(Float)  # ECEF X coordinate in meters
    y = Column(Float)  # ECEF Y coordinate in meters
    z = Column(Float)  # ECEF Z coordinate in meters
    error = Column(Float)  # position accuracy in meters