from __future__ import annotations

from abc import abstractmethod, ABC
from open_precision.core.interfaces.sensor_types.basic_sensor import BasicSensor
from open_precision.core.model.location import Location


class GlobalPositioningSystem(BasicSensor, ABC):
    @property
    @abstractmethod
    def location(self) -> Location:
        """returns a Location object"""
        pass
