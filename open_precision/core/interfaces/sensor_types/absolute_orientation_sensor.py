from abc import abstractmethod, ABC
import numpy as np
from pyquaternion import Quaternion

import open_precision


class AbsoluteOrientationSensor(ABC, open_precision.core.sensor_types.basic_sensor.BasicSensor):
    @property
    @abstractmethod
    def orientation(self) -> Quaternion:
        """returns an orientation quaternion"""
        pass

    @property
    @abstractmethod
    def gravity(self) -> np.ndarray:
        """returns an gravity vector"""
        pass
