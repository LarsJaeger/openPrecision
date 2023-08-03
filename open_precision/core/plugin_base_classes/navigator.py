from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from open_precision.core.model import persist_arg, persist_return
from open_precision.core.model.course import Course
from open_precision.core.model.vehicle_state import VehicleState
from open_precision.core.plugin_base_classes.plugin import Plugin
from open_precision.plugins.course_generators.a_heading_parallel_course_generator import AHeadingParallelCourseGenerator

if TYPE_CHECKING:
    from open_precision.system_hub import SystemHub


class Navigator(Plugin, ABC):
    """computes from current position and target point (or line) to output/call actions that need to be performed in
    order to the target point (or line)"""

    @abstractmethod
    def __init__(self, manager: SystemHub):
        self._manager = manager
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
    @persist_arg
    def course(self, course: Course):
        pass

    @property
    @abstractmethod
    @persist_return
    def target_machine_state(self) -> VehicleState | None:
        pass

    def set_course_from_course_generator(self, course_generator_identifier: str = 'a_heading_parallel'):
        """sets the course generator to the one with the given identifier,
        possible identifiers are: 'a_heading_parallel'"""
        match course_generator_identifier:
            case 'a_heading_parallel':
                self.course = AHeadingParallelCourseGenerator(self._manager).generate_course()
            case _:
                raise ValueError(f'course_generator_identifier {course_generator_identifier} not supported')
