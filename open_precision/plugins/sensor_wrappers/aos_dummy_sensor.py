import numpy as np
from pyquaternion import Quaternion

from open_precision.core.interfaces.sensor_types.absolute_orientation_sensor import AbsoluteOrientationSensor
from open_precision.core.managers.manager import Manager


class AOSDummySensor(AbsoluteOrientationSensor):
    @property
    def orientation(self) -> Quaternion | None:
        return Quaternion()

    @property
    def gravity(self) -> np.ndarray:
        return np.array([0, 0, -1], dtype=np.float64)

    def __init__(self, manager: Manager):
        pass

    def cleanup(self):
        pass
