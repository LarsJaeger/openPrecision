from __future__ import annotations

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from open_precision.core.model.orm.location import ORMLocation
from open_precision.core.model.orm.orm_model_base import ORMModelBase


class ORMPosition(ORMModelBase):
    __tablename__ = 'Positions'

    id = Column(Integer, primary_key=True)

    location = relationship(ORMLocation)
    orientation = Column(String(50))
