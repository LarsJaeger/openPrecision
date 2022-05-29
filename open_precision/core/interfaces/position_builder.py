from abc import abstractmethod, ABC
from typing import TYPE_CHECKING
from open_precision.core.model.position import Position
if TYPE_CHECKING:
    from open_precision.core.managers.manager import Manager


class PositionBuilder(ABC):
    @abstractmethod
    def __init__(self, manager: Manager):
        # self._manager = manager
        pass

    @property
    @abstractmethod
    def current_position(self) -> Position:
        """returns current position (location describes the location of the center of the rear axle)"""
        pass

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        pass
