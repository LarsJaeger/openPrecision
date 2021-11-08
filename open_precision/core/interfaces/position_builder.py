from abc import abstractmethod, ABC
from open_precision.core.model.position import Position
from open_precision.core.plugin_manager import PluginManager


class PositionBuilder(ABC):
    @abstractmethod
    def __init__(self, sensor_manager: PluginManager, config):
        self.sensor_manager = sensor_manager

    @property
    @abstractmethod
    def current_position(self) -> Position:
        """returns current position (location describes the location of the center of the rear axle)"""
        pass

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        pass
