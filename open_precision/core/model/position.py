from __future__ import annotations

from dataclasses import dataclass

from neomodel.properties import validator, Property

from open_precision.core.model import DataModelBase
from open_precision.core.model.location import Location
from open_precision.core.model.orientation import Orientation


@dataclass(kw_only=True)
class Position(DataModelBase):
    """
    A position consists of a location and an orientation.
    """
    location: Location
    orientation: Orientation


class PositionProperty(Property, DataModelBase):
    """
    Property for storing Position objects in Neo4j.
    Position values are stored as a list of 8 floats. The first 4 are the location, the last 4 are the orientation.
    """

    @validator
    def inflate(self, value: list[float]) -> Position:
        return Position(location=Location(value[0], value[1], value[2], value[3]), orientation=Orientation(value[-4:]))

    @validator
    def deflate(self, value: Position) -> list[float]:
        return [value.location.x, value.location.y, value.location.z, value.location.error] + value.q.tolist()
