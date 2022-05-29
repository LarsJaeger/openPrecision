from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from open_precision.core.model.course import Course
if TYPE_CHECKING:
    from open_precision.core.managers.manager import Manager


class CourseGenerator(ABC):
    """Generates a Path and outputs next position based on position (and last actions)"""

    @abstractmethod
    def __init__(self, manager: Manager):
        pass

    @abstractmethod
    def generate_course(self) -> Course:
        pass
