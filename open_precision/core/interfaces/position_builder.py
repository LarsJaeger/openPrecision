from abc import abstractmethod, ABC

from open_precision.core.plugin_manager import PluginManager


class PositionBuilder(ABC):
    @abstractmethod
    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager

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
