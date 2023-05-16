from neomodel import Property
from neomodel.properties import validator
from pyquaternion import Quaternion

from open_precision.core.model.data.data_model_base import DataModelBase


class Orientation(Quaternion, DataModelBase):
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
