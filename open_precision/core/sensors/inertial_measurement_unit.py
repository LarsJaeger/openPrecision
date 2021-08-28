import abc
from abc import ABC, abstractmethod

import numpy as np
import yaml


class InertialMeasurementUnit(ABC):

    @abstractmethod
    def __init__(self, config: yaml):
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
    def is_calibrated(self) -> bool:
        pass

    @abstractmethod
    def calibrate(self) -> bool:
        """calibrate device, (depending on your implementation also set is_calibrated accordingly) and
         return True if calibration succeeded """
        pass
