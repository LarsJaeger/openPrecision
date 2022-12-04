from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

from open_precision.core.model.machine_state import MachineState
from open_precision.core.model.position import Position
from open_precision.core.plugin_base_classes.plugin import Plugin
from open_precision.managers.persistence_manager import PersistenceManager

if TYPE_CHECKING:
    from open_precision.manager import Manager


class MachineStateBuilder(Plugin, ABC):
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
    @PersistenceManager.persist_return
    def machine_state(self) -> MachineState | None:
        # TODO: implement
        return self.current_position

    @property
    @abstractmethod
    @PersistenceManager.persist_return
    def current_position(self) -> Position | None:
        """returns current position (location describes the location of the center of the rear axle)"""
        pass

    @property
    @abstractmethod
    def is_ready(self) -> bool:
        pass
