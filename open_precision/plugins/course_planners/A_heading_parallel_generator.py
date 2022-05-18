import numpy as np

from open_precision.core.interfaces.course_generator import CourseGenerator
from open_precision.core.managers.manager import Manager
from open_precision.core.model.course import Course
from open_precision.core.model.path import Path
from open_precision.core.model.position import Position
from open_precision.core.model.waypoint import Waypoint


class AHeadingParallelGenerator(CourseGenerator):
    def __init__(self, manager: Manager, name: str, description: str, ):
        self.man: Manager = manager

    def generate_course(self) -> Course:
        # get position
        input('press enter to set first position')
        base_position: Position = self.man.position_builder.current_position
        # get user input for working width
        # TODO get user input or read from config
        working_width: float = 3.0

        name = "A+heading C1"

        description = "asdasda"

        course = Course(name=name, description=description, paths=[])
        for i in range(0, 20):
            current_path = Path()
            waypoint = base_position.location \
                       + (1000 * base_position.orientation.rotate(np.ndarray([1, 0, 0])))
            current_path.add_waypoint(Waypoint(location=waypoint))
            waypoint = base_position.location \
                       + (1000 * base_position.orientation.rotate(np.ndarray([1, 0, 0])))
            current_path.add_waypoint(Waypoint(location=waypoint))

            course.add_path(current_path)
        return course
