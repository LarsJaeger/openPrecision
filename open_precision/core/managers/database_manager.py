from __future__ import annotations

import os
from typing import TYPE_CHECKING

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, registry

from open_precision.core.model.vehicle import Vehicle

if TYPE_CHECKING:
    from open_precision.core.managers.manager import Manager


class DatabaseManager:
    def __init__(self, manager: Manager):
        self._man = manager

        self._engine = create_engine('sqlite:///data.sqlite',
                                     echo=True)
        self._init_model()
        self._session_maker = sessionmaker(bind=self._engine)

        v = Vehicle(name="abc", gps_receiver_offset=[5, 6, 7],
                    turn_radius_left=2.1,
                    turn_radius_right=2.3, wheelbase=3.0)

    def _init_model(self):
        mapper_registry = registry()

        mapper_registry.mapped(Vehicle)


        mapper_registry.metadata.create_all(bind=self._engine)

    @property
    def session(self) -> Session:
        return self._session_maker()
