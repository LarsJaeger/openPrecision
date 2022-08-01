from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING
from open_precision.core.model.data.position import Position
from open_precision.core.plugin_base_classes.plugin import Plugin

if TYPE_CHECKING:
    from open_precision.manager import Manager


class PositionBuilder(Plugin, ABC):
    @abstractmethod
    def __init__(self, manager: Manager):
        # self._manager = manager
        # atexit.register(self.cleanup)
        pass

    @abstractmethod
    def cleanup(self):
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