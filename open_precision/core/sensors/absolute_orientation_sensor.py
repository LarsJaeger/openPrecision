from abc import abstractmethod

import numpy as np
import yaml
from pyquaternion import Quaternion

from open_precision import utils
from open_precision.wrappers.wmmToolWrapper import WmmToolWrapper


class AbsoluteOrientationSensor:
    @abstractmethod
    def __init__(self, config):
        pass

    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod(property)
    def scaled_acceleration(self) -> np.ndarray:
        pass

    @abstractmethod(property)
    def scaled_angular_acceleration(self) -> np.ndarray:
        pass

    @abstractmethod(property)
    def scaled_magnetometer(self) -> np.ndarray:
        pass

    @abstractmethod(property)
    def orientation(self) -> Quaternion:
        """returns an orientation quaternion"""
        pass

    @abstractmethod(property)
    def gravity(self) -> np.ndarray:
        """returns an gravity vector"""
        pass

    @abstractmethod(property)
    def is_calibrated(self) -> bool:
        pass

    @abstractmethod
    def calibrate(self) -> bool:
        """calibrate device, (depending on your implementation also set is_calibrated accordingly) and
         return True if calibration succeeded"""
        pass