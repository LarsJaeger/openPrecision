from __future__ import annotations

from abc import abstractmethod, ABC
import numpy as np
from open_precision.core.interfaces.sensor_types.basic_sensor import BasicSensor


class InertialMeasurementUnit(BasicSensor, ABC):
    @property
    @abstractmethod
    def scaled_acceleration(self) -> np.array:
        pass

    @property
    @abstractmethod
    def scaled_angular_acceleration(self) -> np.array:
        pass

    @property
    @abstractmethod
    def scaled_magnetometer(self) -> np.array:
        pass
