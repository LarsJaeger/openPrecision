from __future__ import annotations

from abc import abstractmethod, ABC
import numpy as np
from pyquaternion import Quaternion

from open_precision.core.interfaces.sensor_types.basic_sensor import BasicSensor


class AbsoluteOrientationSensor(BasicSensor, ABC):
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
