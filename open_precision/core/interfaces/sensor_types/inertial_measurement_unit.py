from __future__ import annotations

from abc import abstractmethod, ABC
import numpy as np

from open_precision.core.plugin import Plugin


class InertialMeasurementUnit(Plugin, ABC):
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
