from __future__ import annotations

import ast
from dataclasses import dataclass, field

from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import registry

from open_precision.core.model.model import Model


def start_mapping(mapper_registry):
    mapper_registry.mapped(Vehicle)


@dataclass
class Vehicle(Model):
    # for SQLAlchemy purposes; __sa_dataclass_metadata_key__ is inherited from 'Model'-class
    __tablename__ = 'Vehicles'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})

    name: str = field(metadata={'sa': Column(String(50))})
    turn_radius_left: float = field(metadata={'as': Column(Float())})
    turn_radius_right: float = field(metadata={'as': Column(Float())})
    wheelbase: float = field(metadata={'as': Column(Float())})  # wheelbase in meters
    """3d vector from the rotation point of the vehicle (normally middle of the rear axle a tractor) at ground height 
    """
    _gps_receiver_offset: str = field(init=False, metadata={'sa': Column(String(50))})
    gps_receiver_offset: list[float]

    @property
    def gps_receiver_offset(self) -> list[float]:
        return list(ast.literal_eval(self._gps_receiver_offset))

    @gps_receiver_offset.setter
    def gps_receiver_offset(self, gps_receiver_offset: list[float]):
        self._gps_receiver_offset = repr(gps_receiver_offset)
