from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from neomodel import Property
from neomodel.properties import validator
from pyquaternion import Quaternion

from open_precision.core.model import DataModelBase


@dataclass(kw_only=True)
class Orientation(Quaternion, DataModelBase):
    q: np.ndarray = None  # will never be None after init, this is just a placeholder for the ClassRegistry
    pass


class OrientationProperty(Property):
    """
    Property for storing Orientation objects in Neo4j
    Orientation Quaternion values are stored as a list of 4 floats.
    """

    @validator
    def inflate(self, value: list[float]) -> Orientation:
        return Orientation(value)

    @validator
    def deflate(self, value: Orientation) -> list[float]:
        return value.q.tolist()
