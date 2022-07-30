from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pyquaternion import Quaternion
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from open_precision.core.model.data_classes.location import Location
from open_precision.core.model.data_classes.model_base import Model


class DAOPosition:
    __tablename__ = 'Positions'

    id = Column(Integer, primary_key=True)

    location = relationship(Location)
    orientation = Column(String(50))
