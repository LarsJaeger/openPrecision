from __future__ import annotations

import numpy as np

from open_precision.core.plugin_base_classes.course_generator import CourseGenerator
from open_precision.core.plugin_base_classes.position_builder import PositionBuilder
from open_precision.manager import Manager
from open_precision.core.model.data_classes.course import Course
from open_precision.core.model.data_classes.path import Path
from open_precision.core.model.data_classes.position import Position
from open_precision.core.model.data_classes.waypoint import Waypoint


class AHeadingParallelGenerator(CourseGenerator):
    def cleanup(self):
        pass

    def __init__(self, manager: Manager):
        self.man: Manager = manager

    def generate_course(self) -> Course:
        # get position
        # input('press enter to set first position')
        print("[INFO]: course generation startet")
        base_position: Position = self.man.plugins[PositionBuilder].current_position
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

        return course
