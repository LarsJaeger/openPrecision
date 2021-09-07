from abc import abstractmethod, ABC

from open_precision.core.sensor_manager import SensorManager


class PositionBuilder(ABC):
    @abstractmethod
    def __init__(self, sensor_manager: SensorManager):
        self.sensor_manager = sensor_manager

    @property
    @abstractmethod
    def current_position(self):
        """returns current position (location describes the location of the center of the rear axle)"""
        # TODO
        pass

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        pass
