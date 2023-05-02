import numpy as np
from pyquaternion import Quaternion

from open_precision.core.plugin_base_classes.sensor_types.absolute_orientation_sensor import AbsoluteOrientationSensor
from open_precision.managers.system_manager import SystemManager


class AOSDummySensor(AbsoluteOrientationSensor):
    @property
    def orientation(self) -> Quaternion | None:
        return Quaternion(0, 0, 0, 1)

    @property
    def gravity(self) -> np.ndarray | None:
        return np.array([0, 0, -1], dtype=np.float64)

    def __init__(self, manager: SystemManager):
        pass

    def cleanup(self):
        pass
