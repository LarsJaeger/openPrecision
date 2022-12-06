from pyquaternion import Quaternion

from open_precision.core.model.data_model_base import DataModelBase


class Orientation(Quaternion, DataModelBase):
    pass
