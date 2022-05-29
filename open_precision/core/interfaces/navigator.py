from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from open_precision.core.model.course import Course
if TYPE_CHECKING:
    from open_precision.core.managers.manager import Manager


class Navigator(ABC):
    """computes from current position and target point (or line) to output/call actions that need to be performed in
    order to the target point (or line)"""

    @abstractmethod
    def __init__(self, manager: Manager):
        pass

    @property
    @abstractmethod
    def course(self) -> Course:
        pass

    @course.setter
    @abstractmethod
    def course(self, course: Course):
        pass

    @property
    @abstractmethod
    def steering_angle(self) -> float:
        pass
