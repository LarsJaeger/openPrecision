from __future__ import annotations

import numpy as np

from open_precision.core.plugin_base_classes.course_generator import CourseGenerator
from open_precision.core.plugin_base_classes.position_builder import PositionBuilder
from open_precision.core.model.course import Course
from open_precision.core.model.path import Path
from open_precision.core.model.position import Position
from open_precision.core.model.waypoint import Waypoint

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from open_precision.manager import Manager


class AHeadingParallelCourseGenerator(CourseGenerator):
    def cleanup(self):
        pass

    def __init__(self, manager: Manager):
        self.man: Manager = manager

    def generate_course(self) -> Course:
        # get position
        # input('press enter to set first position')
        print("[INFO]: course generation started")
        base_position: Position = self.man.plugins[PositionBuilder].current_position
        while not base_position.is_valid():
            base_position: Position = self.man.plugins[PositionBuilder].current_position
            print("invalid_position")
        # get user input for working width
        # TODO get user input or read from config
        working_width: float = 3.0

        name = "A+heading C1"

        description = "asdasda"

        course = Course(name=name, description=description)
        for i in range(-3, 3):
            loc1 = base_position.location \
                   + (base_position.orientation.rotate(np.array([0, 1, 0], dtype=np.float64)) * (i * working_width))

            loc2 = loc1 + (base_position.orientation.rotate(np.array([1, 0, 0], dtype=np.float64)) * 1000)
            current_path = Path().add_waypoint(Waypoint(location=loc1)).add_waypoint(Waypoint(location=loc2))
            course.add_path(current_path)

        print("[INFO]: course generation finished")
        return course
