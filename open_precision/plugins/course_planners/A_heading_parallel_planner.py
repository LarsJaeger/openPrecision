from open_precision.core.interfaces.course_planner import CoursePlanner
from open_precision.core.managers.manager import Manager
from open_precision.core.model.position import Position
from open_precision.core.model.waypoint import Waypoint


class AHeadingParallelPlanner(CoursePlanner):
    def __init__(self, manager: Manager):
        self.lookahead_distance = None
        self.working_width = None
        self.base_position = None
        self.waypoints
        self.man: Manager = manager

    def generate_course(self):
        # get position
        # TODO wait for user input
        self.base_position: Position = self.man.position_builder.current_position
        # get user input for working width
        # TODO get user input or read from config
        self.working_width: float = 3.0
        self.lookahead_distance: float = 10.0



    def check_waypoint(self, waypoint: Waypoint):
        pass

    def get_waypoint(self, position: Position) -> Waypoint:
        # generate waypoint 50m in front of vehicle on working line
        # decide which multiple of working width is closest to position
        # check which multiple of working width is closest to lookahead location
        pass
