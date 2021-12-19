from abc import abstractmethod, ABC
from open_precision.core.managers.manager import Manager
from open_precision.core.model.position import Position


class PositionBuilder(ABC):
    @abstractmethod
    def __init__(self, manager: Manager):
        self._manager = manager

    @property
    @abstractmethod
    def current_position(self) -> Position:
        """returns current position (location describes the location of the center of the rear axle)"""
        pass

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        pass
