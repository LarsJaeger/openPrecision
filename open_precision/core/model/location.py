from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from sqlalchemy import Column, Float, Integer
from sqlalchemy.orm import registry

from open_precision.core.model.model import Model


def start_mapping(mapper_registry):
    mapper_registry.mapped(Location)


mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class Location(Model):
    # for SQLAlchemy purposes; __sa_dataclass_metadata_key__ is inherited from 'Model'-class
    __tablename__ = 'Locations'

    id: int = field(init=False, metadata={'sa': Column(Integer, primary_key=True)})

    x: float = field(metadata={'as': Column(Float)})  # ECEF X coordinate in meters
    y: float = field(metadata={'as': Column(Float)})  # ECEF Y coordinate in meters
    z: float = field(metadata={'as': Column(Float)})  # ECEF Z coordinate in meters
    error: float | None = field(metadata={'as': Column(Float)})  # position accuracy in meters

    def __add__(self, other):
        match other:
            case Location():
                res_x = self.x + other.x
                res_y = self.y + other.y
                res_z = self.z + other.z
                if self.error is not None \
                        and other.error is not None:
                    res_error = self.error + other.error
                else:
                    res_error = None
            case list() | tuple():
                if 3 <= len(other) <= 4 \
                        and self.error is not None \
                        and other[3] is not None:
                    floated_vals = [float(i) for i in other]
                    res_x = self.x + other[0]
                    res_y = self.y + other[1]
                    res_z = self.z + other[2]
                else:
                    raise TypeError
                if len(other) == 4:
                    res_error = self.error + other[3]
                else:
                    res_error = None

            case np.ndarray():
                if 3 <= other.shape[0] <= 4:
                    floated_vals = [float(i) for i in other]
                    res_x = self.x + other[0]
                    res_y = self.y + other[1]
                    res_z = self.z + other[2]
                else:
                    raise TypeError
                if len(other) == 4 \
                        and self.error is not None \
                        and other[3] is not None:
                    res_error = self.error + other[3]
                else:
                    res_error = None
            case _: raise TypeError
        return Location(x=res_x, y=res_y, z=res_z, error=res_error)

    def __sub__(self, other):
        match other:
            case Location():
                res_x = self.x - other.x
                res_y = self.y - other.y
                res_z = self.z - other.z
                if self.error is not None \
                        and other.error is not None:
                    res_error = self.error + other.error
                else:
                    res_error = None
            case list() | tuple():
                if 3 <= len(other) <= 4:
                    floated_vals = [float(i) for i in other]
                    res_x = self.x - other[0]
                    res_y = self.y - other[1]
                    res_z = self.z - other[2]
                else:
                    raise TypeError
                if len(other) == 4 \
                        and self.error is not None \
                        and other[3] is not None:
                    res_error = self.error - other[3]
                else:
                    res_error = None

            case np.ndarray():
                if 3 <= other.shape[0] <= 4:
                    floated_vals = [float(i) for i in other]
                    res_x = self.x - other[0]
                    res_y = self.y - other[1]
                    res_z = self.z - other[2]
                else:
                    raise TypeError
                if len(other) == 4 \
                        and self.error is not None \
                        and other[3] is not None:
                    res_error = self.error + other[3]
                else:
                    res_error = None
            case _:
                raise TypeError
        return Location(x=res_x, y=res_y, z=res_z, error=res_error)

    def to_numpy(self) -> np.array:
        return np.array([self.x, self.y, self.z], dtype=np.float64)
