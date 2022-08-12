from dataclasses import dataclass

from pyquaternion import Quaternion

from open_precision.core.model.data_model_base import DataModelBase


@dataclass
class Orientation(DataModelBase, Quaternion):
    pass
