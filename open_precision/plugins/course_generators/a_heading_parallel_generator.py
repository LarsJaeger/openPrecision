from __future__ import annotations

import numpy as np

from open_precision.core.interfaces.course_generator import CourseGenerator
from open_precision.core.interfaces.position_builder import PositionBuilder
from open_precision.core.managers.manager import Manager
from open_precision.core.model.course import Course
from open_precision.core.model.path import Path
from open_precision.core.model.position import Position
from open_precision.core.model.waypoint import Waypoint


class AHeadingParallelGenerator(CourseGenerator):
    def __init__(self, manager: Manager):
        self.man: Manager = manager

    def generate_course(self) -> Course:
        # get position
        input('press enter to set first position')
        base_position: Position = self.man.plugins[PositionBuilder].current_position
        # get user input for working width
        # TODO get user input or read from config
        working_width: float = 3.0

        name = "A+heading C1"

        description = "asdasda"

        course = Course(name=name, description=description, paths=[])
        for i in range(-3, 3):
            loc1 = base_position.location \
                   + (base_position.orientation.rotate(np.array([0, 1, 0], dtype=np.float64)) * (i * working_width))

            loc2 = loc1 + (base_position.orientation.rotate(np.array([1, 0, 0], dtype=np.float64)) * 1000)
            current_path = Path().add_waypoint(Waypoint(location=loc1)).add_waypoint(Waypoint(location=loc2))
            course.add_path(current_path)


        return course
