from __future__ import annotations

from abc import abstractmethod, ABC
import numpy as np

from open_precision.core.model.orientation import Orientation
from open_precision.core.plugin_base_classes.plugin import Plugin


class AbsoluteOrientationSensor(Plugin, ABC):

    @property
    @abstractmethod
    def orientation(self) -> Orientation | None:
        """returns an orientation quaternion"""
        pass

    @property
    @abstractmethod
    def gravity(self) -> np.ndarray | None:
        """returns an gravity vector"""
        pass
