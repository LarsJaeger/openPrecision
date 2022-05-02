from open_precision.core.interfaces.navigator import Navigator
from open_precision.core.managers.manager import Manager
from open_precision.core.model.course import Course
from open_precision.core.model.path import Path
from open_precision.core.model.position import Location, Position


def calc_distance(loc1: Location, loc2: Location):
    return abs(loc2 - loc1)

def calc_position_error(pos1: Position, pos2: Position):
    # returns a value that becomes bigger the more effort it takes to reach a certain position.
    # wheight of errors: 1. location 2. heading TODO: think of exact balancing of both
    # calc offset:
    offset_error = calc_distance(pos1.location, pos2.location)
    # calc *horizontal* heading error; horizon is a plane that has the vector of pos1 as a normal vector
    heading_error = pos1.orientation * pos2.orientation.inverse
    # TODO convert heading_error (Quaternion) to a scalar that describes the error


def calc_error_optimization_operation():
    # TODO
    pass

class PurePursuitNavigator(Navigator):
    def __init__(self, manager: Manager):
        super().__init__(manager)
        self._manager = manager
        self._course: Course = None
        self._current_path_id = None

    @property
    def course(self):
        return self._course

    @course.setter
    def course(self, course: Course):
        self._course = course

    @property
    def _lookahead_distance(self):
        # TODO make dynamic
        return 10

    def get_steering_angle(self):
        current_position = self._manager.position_builder.current_position
        # TODO maybe add lookahead to current position
        if self._current_path_id is None:
            # TODO get next path
            # check priority
            # look for closest
            pass
        else:
            current_path_waypoints = self._course.paths[self._current_path_id].waypoints
            nearest_waypoint = (None, None)
            for waypoint_id in range(len(current_path_waypoints)):
                # check for closest to lookahead
                if nearest_waypoint[1] is None:
                    nearest_waypoint = (waypoint_id,
                                        calc_distance(current_position.location,
                                                      current_path_waypoints[waypoint_id].location))
                else:
                    waypoint_distance = calc_distance(current_position.location,
                                                      current_path_waypoints[waypoint_id].location)
                    if waypoint_distance < nearest_waypoint[1]:
                        nearest_waypoint = (waypoint_id, waypoint_distance)
            second_waypoint = None
            if nearest_waypoint[0] == 0:
                second_waypoint = 1
            elif nearest_waypoint == len(current_path_waypoints) - 1:
                second_waypoint = len(current_path_waypoints) - 2
            else:
                # test if line from waypoint_id - 1 to waypoint_id or from waypoint_id to waypoint_id + 1 is the one to follow
                pass
        # get next waypoint
        # return result of formula (2*|gy|) / L²
        return None
