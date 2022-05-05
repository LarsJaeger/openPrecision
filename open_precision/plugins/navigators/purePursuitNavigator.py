import numpy as np

from open_precision.core.interfaces.navigator import Navigator
from open_precision.core.managers.manager import Manager
from open_precision.core.model.course import Course
from open_precision.core.model.path import Path
from open_precision.core.model.position import Location, Position


def calc_distance(loc1: Location, loc2: Location):
    return abs(loc2 - loc1)


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
                # test if line from waypoint_id - 1 to waypoint_id or from waypoint_id to waypoint_id + 1 is the one
                # to follow
                if self.calc_position_error(current_position, ) # TODO determine location on path that is closest to current_position

                pass
        # get next waypoint
        # return result of formula (2*|gy|) / L²
        return None

    def calc_position_error(self, pos1: Position, target_location: Location, target_direction_vector: np.ndarray) -> float:
        """ returns a value that becomes bigger the more effort it takes to reach a certain position. """
        # calculate offset:
        offset_error = calc_distance(pos1.location, target_location)

        # norm target_direction_vector
        target_direction_vector = np.linalg.norm(target_direction_vector)
        # calc *horizontal* heading error; horizon is a plane that has the vector of pos1 as a normal vector
        relative_orientation_vector = pos1.orientation.inverse.rotate(np.linalg.norm(target_direction_vector))

        """decide which turning radius to use (left or right):
        take direction vector of current waypoints, rotate it by the inverse of vehicle orientation and compare
        components to determine which way to turn"""
        heading_error = relative_orientation_vector[1] * (1 if relative_orientation_vector[0] < 0 else -1)
        if heading_error < 0:
            turning_radius = self._manager.vehicles.current_vehicle.turn_radius_right
        else:
            turning_radius = self._manager.vehicles.current_vehicle.turn_radius_left

        # factor that describes the change of radius TODO make dependent on current speed
        speed_turning_radius_factor = 1.1
        # calculate angle between vehicle direction and line direction
        heading_error_angle = np.arccos(np.clip(np.dot(relative_orientation_vector, np.ndarray([1, 0, 0])), -1.0, 1.0))
        # final_error = e_o + 1XX% r_min * (2 * e_h / pi)
        final_error = offset_error + np.multiply(np.multiply(speed_turning_radius_factor, turning_radius),
                                                 np.divide(heading_error_angle, np.pi))
        return final_error
