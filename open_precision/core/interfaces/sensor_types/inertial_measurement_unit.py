from abc import abstractmethod, ABC
import numpy as np
from open_precision.core.interfaces.basic_sensor import BasicSensor


class InertialMeasurementUnit(BasicSensor, ABC):
    @property
    @abstractmethod
    def scaled_acceleration(self) -> np.ndarray:
        pass

    @property
    @abstractmethod
    def scaled_angular_acceleration(self) -> np.ndarray:
        pass

    @property
    @abstractmethod
    def scaled_magnetometer(self) -> np.ndarray:
        pass
