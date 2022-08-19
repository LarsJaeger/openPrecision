from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from open_precision.core.model.course import Course
from open_precision.core.model.machine_state import MachineState
from open_precision.core.plugin_base_classes.plugin import Plugin
from open_precision.managers.persistence_manager import PersistenceManager

if TYPE_CHECKING:
    from open_precision.manager import Manager


class Navigator(Plugin, ABC):
    """computes from current position and target point (or line) to output/call actions that need to be performed in
    order to the target point (or line)"""

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
    def course(self) -> Course:
        pass

    @course.setter
    @abstractmethod
    @PersistenceManager.persist_arg
    def course(self, course: Course):
        pass

    @property
    @abstractmethod
    @PersistenceManager.persist_return
    def target_machine_state(self) -> MachineState | None:
        pass
