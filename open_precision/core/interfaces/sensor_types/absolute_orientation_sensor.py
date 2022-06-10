from __future__ import annotations

from abc import abstractmethod, ABC
import numpy as np
from pyquaternion import Quaternion

from open_precision.core.plugin import Plugin


class AbsoluteOrientationSensor(Plugin, ABC):
    @property
    @abstractmethod
    def orientation(self) -> Quaternion | None:
        """returns an orientation quaternion"""
        pass

    @property
    @abstractmethod
    def gravity(self) -> np.ndarray | None:
        """returns an gravity vector"""
        pass
