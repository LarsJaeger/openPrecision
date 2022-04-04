import numpy as np

from open_precision.core.interfaces.course_planner import CoursePlanner
from open_precision.core.managers.manager import Manager
from open_precision.core.model.course import Course
from open_precision.core.model.path import Path
from open_precision.core.model.position import Position
from open_precision.core.model.waypoint import Waypoint


class AHeadingParallelPlanner(CoursePlanner):
    def __init__(self, manager: Manager):
        super().__init__(manager)
        self.name = None
        self.description = None
        self.lookahead_distance = None
        self.working_width = None
        self.base_position = None
        self.course = None
        self.man: Manager = manager

    def generate_course(self):
        # get position
        # TODO wait for user input
        self.base_position: Position = self.man.position_builder.current_position
        # get user input for working width
        # TODO get user input or read from config
        self.working_width: float = 3.0

        self.name = "A+heading C1"

        self.description = "asdasda"

        self.course = Course(name=self.name, description=self.description, paths=[])
        for i in range(0, 20):
            current_path = Path()

            waypoint = self.base_position.location \
                       + (1000 * self.base_position.orientation.rotate(np.ndarray([1, 0, 0])))
            current_path.add_waypoint(Waypoint(location=waypoint))

            waypoint = self.base_position.location \
                       + (1000 * self.base_position.orientation.rotate(np.ndarray([1, 0, 0])))
            current_path.add_waypoint(Waypoint(location=waypoint))

            self.course.add_path(current_path)

    def check_waypoint(self, waypoint: Waypoint):
        pass

    def get_waypoint(self, position: Position) -> Waypoint:
        # generate waypoint 50m in front of vehicle on working line
        # decide which multiple of working width is closest to position
        # check which multiple of working width is closest to lookahead location
        pass
