from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from open_precision.core.model.machine_state import MachineState
from open_precision.core.plugin_base_classes.course_generator import CourseGenerator
from open_precision.core.plugin_base_classes.plugin import Plugin
from open_precision.managers.action_manager import ActionManager
from open_precision.managers.persistence_manager import PersistenceManager
from open_precision.plugins.course_generators.a_heading_parallel_course_generator import AHeadingParallelCourseGenerator

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
    def course(self) -> CourseGenerator:
        pass

    @course.setter
    @abstractmethod
    @PersistenceManager.persist_arg
    def course(self, course: CourseGenerator):
        pass

    @property
    @abstractmethod
    @PersistenceManager.persist_return
    def target_machine_state(self) -> MachineState | None:
        pass

    @ActionManager.enable_action
    def set_course_from_course_generator(self, course_generator_identifier: str = 'a_heading_parallel'):
        """sets the course generator to the one with the given identifier,
        possible identifiers are: 'a_heading_parallel'"""
        match course_generator_identifier:
            case 'a_heading_parallel':
                self.course = AHeadingParallelCourseGenerator(self._manager).generate_course()
            case _:
                raise ValueError(f'course_generator_identifier {course_generator_identifier} not supported')
